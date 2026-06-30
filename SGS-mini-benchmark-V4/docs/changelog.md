# Changelog

## v4.0.0 - SGS-100 Final Dataset

- Added `data/benchmark.json` as the single active benchmark file.
- Added `data/benchmark.csv` as the table review format.
- Consolidated the active release to 100 items.
- Matched the ChemBench mini type proportions after rounding: 82 multiple-choice items and 18 free-response items.
- Preserved the ChemBench-like domain proportions in semiconductor gas-sensing form.
- Rewrote MCQ options to satisfy length balance, local-plausibility, anti-leakage, and answer-balance constraints.
- Added consistency groups for humidity drift, carrier direction, data-boundary reasoning, and toxic-gas safety.
- Updated default runner, scorer, validation, README, dataset card, overview, methodology, and scoring rubric to use SGS-100.
- Kept V3 as the repository root project and placed V4 in this independent subfolder.
