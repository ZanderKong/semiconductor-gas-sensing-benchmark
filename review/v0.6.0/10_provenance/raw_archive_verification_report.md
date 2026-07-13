# Raw Archive Verification Report

- Archive SHA-256: `9cbaba75d0ade9b2c8673cf54c06e991e616b3e1180d416ae374101debccc103`
- ZIP integrity: **pass**; members: **46**
- Rebuilt rows: MCQ 488; free-response 120; Robustness 160; Hard50 200.
- Judge reviews: 120 unique rows.
- DeepSeek `SGS-081`: raw answer is empty; deterministic no-rescue total is 0.
- Raw-to-derived field differences: **0**.

The archived `artifact_generation_working_tree_dirty=true` flag belongs to a later `--reuse-raw` artifact-generation pass. The raw run itself records a clean tree. This replay reconstructs every deterministic row from the archive and checks it against the committed outputs.
