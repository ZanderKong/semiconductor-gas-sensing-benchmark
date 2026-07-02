# Model Error Analysis

## Main Error Families

| Error Family | Mechanism | Benchmark Signal |
|---|---|---|
| High-information rule compression | A short prompt compresses a domain convention, spectrum pattern, or hidden condition | Model selects a semantically adjacent rule |
| Quantitative precision loss | Units, signs, coefficients, or final-answer format must all align | Model reports an intermediate value or near miss |
| Structure-property extraction error | The answer depends on reading structural features or molecular-option properties | Model follows generic development language |
| Expert boundary-condition transfer | A valid rule is applied outside its current boundary | Model chooses a locally plausible option |
| Safety specificity error | Several options sound safety-related, but only one is the first-order risk | Model selects broad caution rather than the operative risk |

## Model-Level Pattern

DeepSeek V4 Pro has the highest Scientific Stress MCQ score, suggesting stronger recovery on some rule-bound and quantitative items. GPT-5.5 has the strongest Domain Core MCQ score but the lowest Scientific Stress MCQ score, showing a larger gap between domain workflow judgment and compact stress mechanisms. MiMo v2.5 Pro has strong robustness performance but remains vulnerable to near-miss distractors in the Scientific Stress Set.

## Item-Level Design Implication

The most useful items create wrong answers that can be explained by a specific mechanism. Low-value items produce either universal correctness or diffuse errors that cannot be traced to a stable design feature.

Future pruning should keep items with stable separation, clear error attribution, and domain-relevant constraints. Items with shallow lexical cues or redundant failure mechanisms should be archived.
