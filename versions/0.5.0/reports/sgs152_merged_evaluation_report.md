# SGS152 Merged Evaluation Report

## Purpose

SGS152 merges the legacy SGS100 professional layer with a 52-item failure-mined design bank. The goal is to preserve domain realism while increasing discrimination among strong models.

## Composition

| Component | Items | MCQ | Free-response |
|---|---:|---:|---:|
| Legacy SGS100 | 100 | 82 | 18 |
| Failure-mined design bank | 52 | 40 | 12 |
| Active SGS152 | 152 | 122 | 30 |

The added items use IDs `SGS-FM-001` through `SGS-FM-052`. Their metadata records design family, design insight, option rationales, and rubric information without source provenance.

## Three-Model MCQ Results

| Model | Correct / Total | Accuracy | Safety Fail Rate |
|---|---:|---:|---:|
| DeepSeek V4 Pro | 98 / 122 | 80.3% | 0.0% |
| GPT-5.5 | 95 / 122 | 77.9% | 0.0% |
| MiMo v2.5 Pro | 93 / 122 | 76.2% | 6.2% |

## Split Results

| Model | Legacy SGS MCQ | Failure-mined MCQ |
|---|---:|---:|
| DeepSeek V4 Pro | 77 / 82 | 21 / 40 |
| GPT-5.5 | 80 / 82 | 15 / 40 |
| MiMo v2.5 Pro | 77 / 82 | 16 / 40 |

## Interpretation

The failure-mined MCQ layer is substantially harder than the legacy domain layer. This confirms the central iteration lesson: reskinning can make a hard item easier by adding familiar context or removing the original pressure structure. Preserving the failure mechanism gives a clearer signal for strong-model comparison.

## Next Actions

- Score the 30 free-response items with the rubric protocol.
- Retain items that create stable model separation.
- Remove items that all strong models answer correctly with shallow or identical reasoning.
- Add more artificial, realistic lab-observation questions where the correct next action depends on hidden experimental constraints.
