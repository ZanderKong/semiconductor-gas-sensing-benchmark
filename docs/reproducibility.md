# Reproducibility — v0.6.0

## Frozen evidence

- v0.5.0 baseline commit: `dfa28407e5130dbc4328ac006a5368f18bdbff7d`；
- raw archive: `artifacts/SGS152_raw_evidence_20260713.zip`；
- archive SHA-256: `9cbaba75d0ade9b2c8673cf54c06e991e616b3e1180d416ae374101debccc103`；
- archive members: 46（36 files + 10 directories）。

## Deterministic raw rebuild

```bash
python3 review_tools/rebuild_raw_evidence.py \
  --repo-root . \
  --archive artifacts/SGS152_raw_evidence_20260713.zip \
  --out review_outputs/raw_rebuild

python3 review_tools/rebuild_and_compute_full_statistics.py \
  --archive artifacts/SGS152_raw_evidence_20260713.zip \
  --repo-root . \
  --out review_outputs/full_statistics
```

重建会检查 ZIP 完整性、每个成员 SHA-256、任务文件 hash、MCQ `122×4`、free-response `30×4`、Robustness `40×4`、Hard50 `50×4`、120 条唯一 Judge 记录、DeepSeek `SGS-081` 原始缺答与 no-rescue 0，以及所有确定性 derived 文件的逐字段差异。

当前验证结果是 raw-to-derived 差异 0。归档 Judge manifest 中 `artifact_generation_working_tree_dirty=true` 描述的是后续 `--reuse-raw` 派生产物生成时的工作树状态；原始运行自身记录为 clean。干净 worktree 重放得到相同 derived rows，未发现该状态改变评分产物。

## Release validation

```bash
python3 -m py_compile review_tools/*.py scripts/audit_v0_6.py scripts/audit_source_review_packages.py
python3 scripts/validate_benchmark.py
python3 scripts/lint_benchmark.py
python3 scripts/lint_sgs100_benchmark.py
python3 scripts/validate_hard50.py
python3 scripts/final_provenance_audit.py
python3 scripts/audit_source_review_packages.py
python3 scripts/audit_v0_6.py
unzip -tq artifacts/SGS152_raw_evidence_20260713.zip
git diff --check
git status --porcelain
```

重建证据见 [`review/v0.6.0/10_provenance/`](../review/v0.6.0/10_provenance/)，完整统计见 [`review/v0.6.0/08_statistics/generated_statistics/`](../review/v0.6.0/08_statistics/generated_statistics/)。
