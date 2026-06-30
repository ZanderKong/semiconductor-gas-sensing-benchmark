# Agent Modes V4

SGS-100 V4 supports two evaluation modes.

## No-Tool Mode

The model answers from the question and options only. This mode tests baseline professional judgment, evidence-boundary awareness, and safety reasoning without retrieval or calculation support.

## Tool-Allowed Mode

The model may use calculators, table analysis, literature retrieval, plotting, safety references, or protocol checklists when the item metadata marks a tool expectation. Tool use is judged by outcome and trace quality, not by hidden reasoning.

## Reporting

Reports should separate:

- MCQ exact-match accuracy;
- safety fail rate;
- wrong-option profiles;
- domain, stage, and tool-type breakdowns;
- free-response rubric review;
- consistency-group review.

V4 does not require model private chain-of-thought. It records visible inputs, tool calls, tool outputs, final answers, judge decisions, and hashes where useful.
