# Task Design V4

## Scope

V4 is the SGS-100 release: 100 Chinese semiconductor gas-sensing benchmark items, with 82 multiple-choice items and 18 free-response items.

## MCQ Design

Each multiple-choice item has four options. The options are designed so that:

- each option is a concrete research action, judgment, or validation direction;
- each option can be reasonable under some premise;
- wrong options are contextually non-prioritized, insufficient, or overextended rather than absurd;
- option length is balanced and does not reveal the answer;
- answer positions are near-balanced across A/B/C/D.

## Free-Response Design

Free-response items focus on safety, evidence boundaries, experimental controls, table interpretation, route selection, and public-project abstraction. They are not intended for exact-string scoring.

## Consistency Groups

Selected items share `consistency_group_id` fields. These groups test whether a model keeps stable principles across nearby variants, such as humidity drift, carrier type, data-boundary reasoning, and toxic-gas safety.
