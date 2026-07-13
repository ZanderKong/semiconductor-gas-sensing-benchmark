#!/usr/bin/env python3
"""Generate README leaderboard and evaluation-flow SVG assets."""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
MODEL_LABELS = {
    "gpt-5.5": "GPT-5.5",
    "deepseek-v4-pro": "DeepSeek V4 Pro",
    "mimo-v2.5-pro": "MiMo v2.5 Pro",
    "ep-20260703090429-qpmt7": "Seed-2.1",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def leaderboard_svg() -> str:
    rows = read_rows(ROOT / "results/standard_20260703/sgs152_mcq/scored/model_results_summary.csv")
    rows.sort(key=lambda row: float(row["mc_accuracy"]), reverse=True)
    width, height = 1200, 570
    left, top, chart_width, row_gap = 330, 145, 760, 82
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">SGS152 MCQ Main Leaderboard</title>',
        '<desc id="desc">Four participating model accuracy results on the 122-question SGS152 multiple-choice main set.</desc>',
        '<rect width="1200" height="570" rx="28" fill="#f8fafc"/>',
        '<text x="64" y="70" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#0f172a">SGS152 MCQ Main Leaderboard</text>',
        '<text x="64" y="105" font-family="Arial, sans-serif" font-size="18" fill="#475569">122 questions · exact match · main leaderboard only</text>',
    ]
    for tick in range(90, 101, 2):
        x = left + (tick - 90) / 10 * chart_width
        parts.append(f'<line x1="{x:.1f}" y1="125" x2="{x:.1f}" y2="475" stroke="#cbd5e1" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="510" text-anchor="middle" font-family="Arial, sans-serif" font-size="15" fill="#64748b">{tick}%</text>')
    for index, row in enumerate(rows):
        accuracy = float(row["mc_accuracy"]) * 100
        correct = int(row["correct"])
        model = MODEL_LABELS.get(row["model_id"], row["model_id"])
        y = top + index * row_gap
        bar_width = max(0.0, (accuracy - 90) / 10 * chart_width)
        color = "#0f766e" if index == 0 else "#64748b"
        parts.append(f'<text x="300" y="{y + 28}" text-anchor="end" font-family="Arial, sans-serif" font-size="20" font-weight="600" fill="#0f172a">{escape(model)}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{bar_width:.1f}" height="38" rx="10" fill="{color}"/>')
        parts.append(f'<text x="{left + bar_width - 14:.1f}" y="{y + 27}" text-anchor="end" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#ffffff">{correct}/122 · {accuracy:.2f}%</text>')
    parts.append('<text x="64" y="550" font-family="Arial, sans-serif" font-size="14" fill="#64748b">Axis starts at 90%. Live run: 2026-07-03. GPT-5.6-sol is the judge and is not a participating model.</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def flow_svg() -> str:
    nodes = [
        (55, "1  Freeze", "SGS152 + diagnostic sets", "task and prompt hashes"),
        (325, "2  Run", "single sample · temp 0", "no internet or tools"),
        (595, "3  Score", "MCQ exact match", "FR: GPT-5.6-sol judge"),
        (865, "4  Separate", "122 MCQ main leaderboard", "FR · Robustness · Hard50"),
        (1135, "5  Audit", "manifests + raw outputs", "item-level failure records"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="430" viewBox="0 0 1400 430" role="img" aria-labelledby="title desc">',
        '<title id="title">SGS benchmark evaluation flow</title>',
        '<desc id="desc">The evaluation freezes datasets, runs models once without tools, scores each layer separately, and audits hashes and item-level errors.</desc>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b"/></marker></defs>',
        '<rect width="1400" height="430" rx="28" fill="#f8fafc"/>',
        '<text x="55" y="62" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#0f172a">Evaluation flow</text>',
        '<text x="55" y="96" font-family="Arial, sans-serif" font-size="18" fill="#475569">Comparable inputs, separated scores, traceable evidence</text>',
    ]
    for index in range(len(nodes) - 1):
        x1 = nodes[index][0] + 210
        x2 = nodes[index + 1][0] - 18
        parts.append(f'<line x1="{x1}" y1="230" x2="{x2}" y2="230" stroke="#64748b" stroke-width="3" marker-end="url(#arrow)"/>')
    for index, (x, title, line1, line2) in enumerate(nodes):
        fill = "#ccfbf1" if index in {0, 4} else "#e2e8f0"
        stroke = "#0f766e" if index in {0, 4} else "#94a3b8"
        parts.extend([
            f'<rect x="{x}" y="145" width="210" height="170" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
            f'<text x="{x + 18}" y="190" font-family="Arial, sans-serif" font-size="23" font-weight="700" fill="#0f172a">{escape(title)}</text>',
            f'<text x="{x + 18}" y="235" font-family="Arial, sans-serif" font-size="16" fill="#334155">{escape(line1)}</text>',
            f'<text x="{x + 18}" y="268" font-family="Arial, sans-serif" font-size="16" fill="#334155">{escape(line2)}</text>',
        ])
    parts.append('<text x="700" y="375" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#0f766e">Only SGS152 MCQ enters the headline ranking; diagnostic layers are never collapsed into one score.</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "leaderboard.svg").write_text(leaderboard_svg(), encoding="utf-8")
    (ASSETS / "evaluation_flow.svg").write_text(flow_svg(), encoding="utf-8")
    print("Generated assets/leaderboard.svg and assets/evaluation_flow.svg")


if __name__ == "__main__":
    main()
