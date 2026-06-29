#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX = Path("/Applications/Codex.app/Contents/Resources/codex")


def load_questions(path, question_type="multiple_choice", limit=0):
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    if question_type != "all":
        rows = [row for row in rows if row["question_type"] == question_type]
    if limit:
        rows = rows[:limit]
    return rows


def compact_question(row):
    item = {
        "id": row["id"],
        "question_type": row["question_type"],
        "domain": row["domain"],
        "scenario_stage": row["scenario_stage"],
        "tool_type": row["tool_type"],
        "question": row["question"],
    }
    if row["question_type"] == "multiple_choice":
        item["options"] = row["options"]
    return item


def build_prompt(rows):
    intro = (ROOT / "eval/prompts/base_prompt.md").read_text(encoding="utf-8")
    return intro + "\n\n题目如下：\n" + json.dumps(
        [compact_question(row) for row in rows], ensure_ascii=False
    )


def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def normalize_answers(payload, ids):
    raw = payload.get("answers", payload if isinstance(payload, list) else [])
    answers = {}
    for item in raw:
        if not isinstance(item, dict):
            continue
        qid = str(item.get("id", "")).strip()
        answer = str(item.get("answer", "")).strip().upper().replace("，", ",")
        if qid in ids:
            answers[qid] = answer
    return answers


def call_openai_compatible(model_id, base_url, api_key, prompt, temperature=0, timeout=900):
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["choices"][0]["message"]["content"]


def call_codex(model_id, prompt, timeout=900):
    if not CODEX.exists():
        raise RuntimeError(f"Codex CLI not found at {CODEX}")
    with tempfile.TemporaryDirectory(prefix="sgs_bench_") as tmp:
        tmp_path = Path(tmp)
        prompt_path = tmp_path / "prompt.txt"
        out_path = tmp_path / "last_message.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        cmd = [
            str(CODEX),
            "exec",
            "--skip-git-repo-check",
            "--ephemeral",
            "--sandbox",
            "read-only",
            "--ignore-rules",
            "-m",
            model_id,
            "-c",
            'model_reasoning_effort="low"',
            "--output-last-message",
            str(out_path),
            "-",
        ]
        with prompt_path.open("r", encoding="utf-8") as stdin:
            proc = subprocess.run(
                cmd,
                cwd=tmp_path,
                stdin=stdin,
                text=True,
                capture_output=True,
                timeout=timeout,
            )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr[-2000:])
        return out_path.read_text(encoding="utf-8")


def run_one(model, rows, args):
    prompt = build_prompt(rows)
    started = time.time()
    if model["provider"] == "codex_cli":
        text = call_codex(model["model_id"], prompt, args.timeout)
    else:
        key = os.environ.get(model["api_key_env"], "")
        if not key:
            raise RuntimeError(f"Missing env var {model['api_key_env']}")
        text = call_openai_compatible(
            model["model_id"],
            model["base_url"],
            key,
            prompt,
            temperature=args.temperature,
            timeout=args.timeout,
        )
    elapsed = round(time.time() - started, 2)
    payload = extract_json(text)
    answers = normalize_answers(payload, {row["id"] for row in rows})
    return text, answers, elapsed


def default_models():
    return [
        {"provider": "codex_cli", "model_id": "gpt-5.5"},
        {
            "provider": "openai_compatible",
            "model_id": "deepseek-chat",
            "base_url": "https://api.deepseek.com",
            "api_key_env": "DEEPSEEK_API_KEY",
        },
    ]


def parse_model_spec(spec):
    # provider|model_id|base_url|api_key_env
    parts = spec.split("|")
    if len(parts) == 1:
        return {"provider": "codex_cli", "model_id": spec}
    if len(parts) != 4:
        raise ValueError("Model spec must be provider|model_id|base_url|api_key_env")
    return {
        "provider": parts[0],
        "model_id": parts[1],
        "base_url": parts[2],
        "api_key_env": parts[3],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", default=str(ROOT / "data/benchmark_v1.json"))
    parser.add_argument("--out", default=str(ROOT / "results/model_outputs.csv"))
    parser.add_argument("--raw-dir", default=str(ROOT / "results/raw_model_outputs"))
    parser.add_argument("--question-type", default="multiple_choice", choices=["multiple_choice", "free_response", "all"])
    parser.add_argument("--models", nargs="*", help="Optional provider:model_id:base_url:api_key_env specs")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    rows = load_questions(args.benchmark, args.question_type, args.limit)
    models = [parse_model_spec(spec) for spec in args.models] if args.models else default_models()
    out_path = Path(args.out)
    raw_dir = Path(args.raw_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    output_rows = []
    for model in models:
        label = model["model_id"]
        print(f"running {label} on {len(rows)} {args.question_type} items", flush=True)
        try:
            raw_text, answers, elapsed = run_one(model, rows, args)
            (raw_dir / f"{label.replace('/', '_')}.txt").write_text(raw_text, encoding="utf-8")
            missing = [row["id"] for row in rows if row["id"] not in answers]
            for row in rows:
                output_rows.append(
                    {
                        "id": row["id"],
                        "model_id": label,
                        "provider": model["provider"],
                        "answer": answers.get(row["id"], ""),
                        "elapsed_seconds": elapsed,
                        "error": "",
                    }
                )
            if missing:
                print(f"warning: {label} missing {len(missing)} answers", flush=True)
        except Exception as exc:
            print(f"error: {label}: {exc}", flush=True)
            output_rows.append(
                {
                    "id": "",
                    "model_id": label,
                    "provider": model["provider"],
                    "answer": "",
                    "elapsed_seconds": "",
                    "error": str(exc),
                }
            )

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "model_id", "provider", "answer", "elapsed_seconds", "error"],
        )
        writer.writeheader()
        writer.writerows(output_rows)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
