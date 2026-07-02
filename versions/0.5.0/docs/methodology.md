# Methodology

## Benchmark Construction

SGS 0.5.0 uses a layered benchmark construction method.

| Layer | Construction Method |
|---|---|
| Domain Core Set | Abstract semiconductor gas-sensing R&D tasks into scoreable MCQ and free-response items |
| Scientific Stress Set | Add compact scientific mechanisms that expose rule-boundary, quantitative, structure-property, spectrum-pattern, and safety-risk errors |
| Robustness Set | Generate nearby variants that test whether a model preserves the same judgment principle under paraphrase, distractors, condition updates, and tool observations |
| Hard Diagnostic Set | Target condition update, evidence conflict, safety gate, tool-observation update, tradeoff, and mechanism-transfer failures |

## Item Design

Each item is organized around a decisive constraint. Examples include material mechanism, gas-response evidence, humidity interference, characterization boundary, safety authorization, numerical unit, spectrum pattern, or expert convention.

Distractors are designed to be locally plausible. A distractor may match a keyword, optimize a secondary metric, report an intermediate value, overgeneralize a scientific rule, or apply a valid principle outside its current boundary.

## Error Attribution

Every scored MCQ item includes fields that support error analysis:

| Field | Role |
|---|---|
| `domain` | Scientific or R&D domain |
| `scenario_stage` | Workflow stage |
| `tool_type` | Tool-use expectation |
| `failure_mode` | Primary error mechanism |
| `option_profiles` | Distractor profile by option |
| `option_rationales` | Rationale for correct and incorrect options |

## Scientific Stress Set Design

Scientific Stress Set items are retained when they create stable model separation and interpretable errors. Their metadata records design insight, failure family, distractor logic, and scoring requirements.

## Realistic Lab Observation Items

The seed realistic-observation items show the desired next direction. A paper-strip loading problem with 4-苯氧基苯胺 tests whether the model notices that an aqueous impregnation route can fail because the compound is poorly water soluble. A silver nitrate paper-material problem tests whether the model uses light-reaction particle-size behavior rather than defaulting to an oxide explanation.
