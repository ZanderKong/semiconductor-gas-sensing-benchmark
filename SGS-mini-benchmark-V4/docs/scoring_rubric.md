# Scoring Rubric

## Multiple-Choice Items

MCQ items are scored with exact A/B/C/D matching. The answer alone is not the full diagnostic signal; each item also includes:

- `option_profiles`;
- `option_rationales`;
- `failure_mode`;
- `scenario_stage`;
- `tool_type`;
- optional `consistency_group_id`.

Badcase analysis should report both the wrong option and the reason that option is locally plausible but not optimal in the current context.

## Free-Response Items

Free-response items use rubric-based scoring. A strong answer should:

- answer the requested decision or calculation;
- state the relevant evidence boundary;
- identify missing controls or confounders;
- stay within safety and privacy limits;
- provide an actionable next step when the prompt asks for one.

## Consistency Analysis

Items with the same `consistency_group_id` should be reviewed together. A model that answers each item in isolation but flips the underlying principle across variants should be marked for consistency review.
