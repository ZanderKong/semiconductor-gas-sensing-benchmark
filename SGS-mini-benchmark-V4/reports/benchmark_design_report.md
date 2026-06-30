# Benchmark Design Report

## Design Goal

SGS-100 V4 turns semiconductor gas-sensing R&D judgment into a compact, structured, and reproducible benchmark.

## Key Design Decisions

- Use ChemBench mini proportions as the high-level shape: 82 multiple-choice and 18 free-response items.
- Rewrite all content for semiconductor gas-sensing materials rather than generic chemistry trivia.
- Make each MCQ option a concrete research action, judgment, or validation direction.
- Require distractors to be locally plausible and only contextually non-prioritized, insufficient, or overextended.
- Track workflow stage, tool type, failure mode, safety boundary, and option-level rationale.
- Add explicit consistency fields to every main-set item.
- Add a separate robustness layer for paraphrase, distractor, contradiction, adversarial safety, and tool-observation diagnostics.
- Upgrade every free-response item with a 10-point rubric, key points, hard fails, and common failure modes.
- Preserve V3 in the repository root while publishing V4 as an independent subfolder.

## V4 Implementation

| Layer | Implementation |
|---|---|
| Active data | `data/benchmark.json` and `data/benchmark.csv` |
| Clean export | `data/benchmark_sgs100_clean.csv` and `data/benchmark_sgs100_clean.json` |
| Robustness data | `data/benchmark_sgs100_robustness.csv` and `data/benchmark_sgs100_robustness.json` |
| Free-response rubrics | `data/free_response_rubrics.json` |
| Schema | `data/schema.json` |
| Scoring | `docs/scoring_v4.md` and `docs/dimension_definition.md` |
| Hard Gate | `docs/hard_gates.md` |
| Judge protocol | `docs/judge_protocol.md` |
| Trace and reproducibility | `docs/reproducibility_and_trace.md` |
| Agent mode | `docs/agent_modes.md` |
| Robustness design | `docs/robustness_variant_design.md` |
| Free-response rubric design | `docs/free_response_rubric_design.md` |
| Demo runner | `eval/runner.py` |
| Real-model MCQ runner | `eval/run_eval.py` |
| MCQ scorer | `eval/score_mcq.py` |
| Validation | `scripts/validate_benchmark.py`, `scripts/lint_benchmark.py`, and `scripts/lint_sgs100_benchmark.py` |

## Quality Gates

The active validation checks item count, type distribution, domain distribution, option length balance, forbidden template phrases, answer-position balance, and option rationales.

The clean-revision validation records:

- answer distribution: A=21, B=21, C=20, D=20;
- option length ratio violations: 0;
- robustness variant count: 40;
- free-response rubric count: 18;
- acceptance lint status: passed.

## Model-Evaluation Status

The latest main-set MCQ run uses `deepseek-v4-pro` and `mimo-v2.5-pro`.

MiMo scored 80/82.

DeepSeek scored 76/82.

The robustness run contains 40 variants.

MiMo scored 36/40 on robustness variants.

DeepSeek scored 30/40 on robustness variants.

Kimi was attempted with `kimi-k2.7-code`.

The local environment could not complete a TLS connection to the official Moonshot `.cn` endpoint, and the fallback `.ai` endpoint rejected the supplied key.
