# Iteration Notes

## 0.5.0 Rationale

SGS100 established a compact Domain Core Set for semiconductor gas-sensing R&D judgment. Model scores on the Domain Core MCQ layer became high enough that additional stress mechanisms were needed for frontier-model comparison.

SGS152 adds the Scientific Stress Set to test compact scientific mechanisms that remain difficult for strong models: exact rules, quantitative precision, structure-property extraction, spectrum-pattern recognition, and safety-risk specificity.

## Lessons From Pilot Item Experiments

Full domain transfer can reduce item pressure by adding context, weakening distractors, or turning a precise constraint into a broad R&D recommendation. Mechanism-preserving items produce clearer model separation when the decisive constraint and near-miss distractors remain intact.

## Current Version Status

| Asset | Status |
|---|---|
| SGS152 Main Set | Active |
| Domain Core Set | Stable baseline |
| Scientific Stress Set | Active stress layer |
| Robustness Set | Stability diagnostic |
| Hard Diagnostic Set | Failure-attribution diagnostic |
| Free-response Rubrics | Defined, outside automated leaderboard |

## Next Version Plan

- Add more realistic lab-observation items where the correct next action depends on hidden material properties or preparation constraints.
- Increase table-heavy quantitative tasks and spectrum-pattern tasks.
- Prune MCQ items that all frontier models answer correctly with shallow reasoning.
- Recalibrate Hard Diagnostic Set items toward a stronger target range for frontier models.
- Add sampled rubric reviews for free-response items to validate scoring stability.
