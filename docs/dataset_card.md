# Dataset Card

## Dataset Summary

This repository contains two benchmark layers for evaluating LLMs and agents in Chinese semiconductor gas-sensing materials R&D workflows.

The V1/V2 layer is a 100-item diagnostic benchmark with multiple-choice and free-response questions. The V3-alpha layer contains 46 auditable task units for workflow-oriented agent evaluation.

## Intended Uses

- Evaluate model reasoning in materials R&D workflows.
- Diagnose failures by domain, workflow stage, tool type, and option-trap profile.
- Support controlled comparison across configured model endpoints.

## Out-of-Scope Uses

- Training or fine-tuning models.
- Reconstructing private laboratory formulations.
- Operational guidance for hazardous gas experiments.
- Regulatory or safety certification.

## Data Composition

| Field | Value |
|---|---:|
| V1/V2 total questions | 100 |
| V1/V2 multiple-choice | 82 |
| V1/V2 free-response | 18 |
| V3-alpha task units | 46 |
| V3-alpha static core | 24 |
| V3-alpha robustness variants | 16 |
| V3-alpha live extension | 6 |
| Scenario stages | 6 |
| Private formulation combinations | 0 |

Domain distribution:

| Domain | Count |
|---|---:|
| organic_chemistry | 19 |
| physical_chemistry | 14 |
| inorganic_chemistry | 14 |
| materials_science | 14 |
| general_chemistry | 11 |
| analytical_chemistry | 10 |
| technical_chemistry | 10 |
| toxicity_and_safety | 8 |

## Data Fields

Important fields include:

- `question`, `options`, `answer`, `answer_rationale`
- `domain`, `subfield`, `task_name`
- `scenario_stage`, `workflow_task`, `expected_output`
- `tool_type`
- `option_profiles`, `option_rationales`
- `evaluation_dimensions`, `failure_mode`
- `private_dependency_level`

V3-alpha fields include:

- `task_id`, `benchmark_version`, `benchmark_split`, `task_type`
- `scenario_stage`, `expected_output`, `tool_mode`, `tool_type`
- `target_dimensions`, `hard_gate_checks`, `failure_modes`
- `variant_group_id`, `variant_type`, `source_policy`
- `gold_response`, `scoring_rubric`, `audit_notes`

## Source and Anonymization

The benchmark is built from abstract problem types with private details removed. It covers gas-detection paper tape and semiconductor gas-sensing workflows without including formulation ratios, private sample IDs, customer data, or proprietary experimental conclusions.

Source categories:

- Public chemistry and gas-sensing knowledge.
- Public safety references such as PubChem.
- General analytical chemistry concepts such as LOD and calibration.
- Abstracted workflow patterns from gas paper tape and semiconductor gas-sensing R&D.

## Risks and Limitations

- Multiple-choice items are easier to auto-score but may be less discriminative for strong models.
- Free-response items require human or judge-model review.
- Safety questions are educational evaluation items, not operational SOPs.
- Model results depend on model version, prompt, temperature, and endpoint availability.
- V3-alpha is designed for auditable evaluation units. Real model leaderboard results require a runner configuration, trace capture, and judge protocol.

## Privacy Statement

`private_dependency_level` controls private-context exposure:

| Level | Count |
|---|---:|
| none | 86 |
| analog | 6 |
| seed_entity | 8 |
| private_combination | 0 |

No item contains private formulation combinations.
