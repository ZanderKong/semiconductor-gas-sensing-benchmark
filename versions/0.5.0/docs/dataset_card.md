# Dataset Card

## Dataset

| Field | Value |
|---|---|
| Name | Semiconductor Gas-Sensing Mini-Benchmark |
| Version | 0.5.0 |
| Active main set | SGS152 Main Set |
| Language | Chinese and English |
| Task domain | Semiconductor gas-sensing materials R&D and scientific stress testing |
| Main scoring mode | Automatic MCQ exact match |
| Open-ended review | Rubric-defined, manual or judge-assisted |

## Data Layers

| Logical Layer | File | Items | MCQ | Free-response |
|---|---|---:|---:|---:|
| SGS152 Main Set | `data/benchmark.json` | 152 | 122 | 30 |
| Domain Core Set | `data/benchmark_sgs100_clean.json` | 100 | 82 | 18 |
| Scientific Stress Set | `data/scientific_stress_bank.json` | 52 | 40 | 12 |
| Robustness Set | `data/benchmark_sgs100_robustness.json` | 40 | 40 | 0 |
| Hard Diagnostic Set | `data/benchmark_sgs_hard50.json` | 50 | 50 | 0 |

30 free-response items are rubric-defined and are not included in the current automated MCQ leaderboard.

## Domain Coverage

SGS152 covers organic chemistry, physical chemistry, inorganic chemistry, materials science, general chemistry, analytical chemistry, technical chemistry, toxicity and safety, expert science reasoning, and quantitative science.

## Intended Use

The benchmark evaluates professional judgment in materials R&D tasks: mechanism reasoning, experimental design, evidence-boundary control, data interpretation, safety constraints, route selection, and scientific communication.

## Boundaries

The benchmark does not provide private formulation ratios, internal project identifiers, supplier-sensitive information, or executable hazardous procedures. Safety-related items are designed around go/no-go judgment, evidence sufficiency, and review gates.

## Limitations

SGS152 is a compact benchmark. It emphasizes traceable item mechanisms and model-error attribution rather than broad chemical coverage. Free-response scoring requires rubric review, so the current automated leaderboard should be interpreted as MCQ-only evidence.
