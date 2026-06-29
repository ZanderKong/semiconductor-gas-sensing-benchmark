# Project Overview

Semiconductor Gas-Sensing Agent Benchmark is a compact diagnostic benchmark for Chinese materials R&D workflows. It evaluates whether a model can reason through literature claims, mechanism boundaries, experiment design, abnormal results, next-step planning, safety constraints, and tool use.

The benchmark uses abstract problem types from semiconductor gas-sensing materials. It removes private formulation details, sample identifiers, sensitive procurement details, and unpublished conclusions.

## What The Project Contains

| Module | Purpose |
|---|---|
| V1/V2 benchmark | 100-item Chinese mini benchmark for broad coverage and MCQ pipeline validation |
| V3-alpha task set | 46 auditable task units for workflow-oriented agent evaluation |
| Scoring protocol | Hard Gate, D0-D6 weighted rubric, tool-use scoring, and meta evaluation |
| Demo runner | Local API-free run that generates manifest, trace, judge outputs, report, and badcases |
| Validation scripts | Schema checks, distribution checks, metadata checks, and documentation lint |
| Reports and assets | Human-readable summaries for model behavior and benchmark structure |

## Core Evaluation Ideas

| Layer | Description |
|---|---|
| Hard Gate | Flags unacceptable failures in safety, evidence fabrication, dangerous tool use, privacy leakage, and severe instruction violation |
| D0-D6 scoring | Scores instruction following, professional accuracy, contextual judgment, evidence boundary, actionability, tool use, and safety boundary |
| Tool Use Evaluation | Separates no-tool baseline from tool-enabled agent behavior |
| Trace-Based Audit | Records visible inputs, tool calls, tool observations, model outputs, and judge outputs |
| Robustness And Live Extension | Separates fixed regression tasks from variants and replaceable extension tasks |

## Quick Demo

```bash
make demo
make validate
make lint
make report
```

The demo writes results to:

```text
results/runs/demo/
├── run_manifest.json
├── model_outputs.jsonl
├── judge_outputs.jsonl
├── trace.jsonl
├── aggregate_metrics.json
├── report.md
├── diagnostic_report.md
└── badcases/
```

## Reader Notes

This repository is designed as a benchmark artifact rather than a laboratory protocol. The tasks evaluate model behavior under abstracted materials R&D scenarios. The files do not provide operational instructions for hazardous gas experiments.

