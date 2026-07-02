# Release Readiness Audit

## Scope

This audit checks whether 0.5.0 is ready for GitHub publication as a coherent benchmark package.

## Readiness Checklist

| Item | Status |
|---|---|
| Active benchmark is self-contained | Ready |
| Build script uses repository-contained inputs | Ready |
| GPT-5.5 SGS152 retry completed | Ready |
| Three-model MCQ summaries updated | Ready |
| Source provenance removed from failure-mined items | Ready |
| README and dataset card aligned | Ready |
| Validation/lint commands available | Ready |
| Raw local traces excluded from release scope | Ready |

## Required Checks

```bash
make validate
make validate-hard50
make lint
make lint-sgs100
make score-mcq
```

## Release Notes

SGS152 should be presented as a 0.5.0 release candidate: strong enough to demonstrate design direction and model differentiation, but still intended for iterative pruning. The next pruning pass should remove low-discrimination items after more model runs.
