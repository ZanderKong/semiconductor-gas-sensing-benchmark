# Dataset Card

## Dataset Summary

This dataset is a 100-item diagnostic benchmark for evaluating LLMs in Chinese semiconductor gas-sensing materials R&D workflows. It includes multiple-choice and free-response questions covering chemistry, materials science, analytical characterization, process engineering, and laboratory safety.

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
| Total questions | 100 |
| Multiple-choice | 82 |
| Free-response | 18 |
| Domains | 8 |
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

## Privacy Statement

`private_dependency_level` controls private-context exposure:

| Level | Count |
|---|---:|
| none | 86 |
| analog | 6 |
| seed_entity | 8 |
| private_combination | 0 |

No item contains private formulation combinations.
