# v0.6.0 Final Consistency Review

## 1. Current baseline

- audit starting HEAD: `24460ff29f1e1840a6c5f6d81779e2ac4b7d8153`;
- branch: `main`;
- version: `0.6.0`;
- legacy evidence baseline only: `dfa28407e5130dbc4328ac006a5368f18bdbff7d`;
- starting and ending worktree status are recorded by the release validation; the audit began clean.

## 2. Source-package mapping

The four user-supplied archives are byte-identical to the exact copies in `review/internal_provenance/source_packages/`. They contain 118 file members. The complete per-member mapping, source and repository hashes, and disposition are in `review/internal_provenance/final_source_package_repository_mapping.csv`.

Comparison counts: `historical_or_source_only`=84, `identical_file`=3, `repository_equivalent_formatting`=8, `repository_role_normalized`=17, `repository_updated_completed_statistics`=2, `repository_updated_public_dashboard`=4. Repository-missing mapped files: `0`. Unresolved content conflicts: `0`.

## 3. Content already present

- item validity: 242 total = 152 main + 40 Robustness + 50 Hard50;
- MCQ: 122 item summaries, 488 option rows, 56 defensible non-Gold options;
- Reference Answer: 30 item rows, 112 claim rows, source ledger and gap queue;
- free-response: 120 item rows, 960 dimension rows, 15 historical Hard Fails = 3 confirmed + 12 downgraded, and one no-answer;
- diagnostics: 40 Robustness pair rows, 12 group rows and 50 Hard50 calibration rows;
- provenance: 46 raw ZIP members, 120 unique Judge rows and zero raw-to-derived field differences.

## 4. New closing evidence

- final per-package repository mapping;
- final `review/v0.6.0` file inventory with SHA-256;
- automatically calculated consistency metrics;
- removal of an unused future-role placeholder and its audit allowance.

No scientific review row, score, Hard Fail decision or frozen benchmark field was changed.

## 5. Historical or duplicate package material

Package READMEs, final reports, manifests, checksum lists, integration handoffs, draft release documents, superseded helper scripts and package-only supporting ledgers remain in the exact internal ZIPs. They were not copied over the current release tree and do not create duplicate release directories.

## 6. Conflict handling

Byte differences were accepted only when parsed CSV content was equivalent, public role fields were normalized, dashboards were role-normalized, or completed statistics superseded package placeholders. Any other mapped difference is classified as `content_conflict`; the final count is `0`.

## 7. Files changed in this closing review

- internal source-package mapping, repository inventory and calculated metrics;
- this final consistency report;
- role registry, integration generator and v0.6 audit logic to remove the unused role placeholder;
- release manifest after adding this report.

## 8. Frozen files not modified

Questions, options, Gold Answers, Reference Answers, item IDs and original model outputs were not modified. Frozen hashes remain release gates in `scripts/audit_v0_6.py`.

## 9. Tests and audits

Validation status: `passed`. The required make targets, provenance audit, v0.6 audit, source-package SHA/Manifest verification, raw rebuild, full-statistics diff, manifest regeneration check and clean-worktree check are release gates.

## 10. Numeric consistency

All figures in this report are generated from the final CSV/JSON artifacts. Machine-readable values are in `review/internal_provenance/final_consistency_metrics.json`.

## 11. Reviewer-role naming

Current public scientific review uses only `专家 X`; project decisions use `项目负责人`; deterministic integration uses `复核者`; GPT-5.6-sol is explicitly the Judge. This review does not disclose the underlying identity of `专家 X` and does not claim independent blind review.

## 12. Known Limitations

The release retains the five frozen P0 records (`SGS-FM-034`, `SGS-007-R03`, `SGS-097-R03`, `SGS-HARD-016`, `SGS-HARD-028`), 56 defensible non-Gold options, two Robustness P0 variants, saturated Hard50 status and the absence of an independent blind-review design.

## 13. Final diff

The exact `git diff --stat` is reported in the delivery response after the closing commit. No generated release artifact remains unexplained.

## 14. Final commit

The final commit SHA is reported in the delivery response because a commit cannot contain its own SHA without changing that SHA.

## 15. Pending items

No v0.6.0 release blocker remains. Known frozen-content issues stay disclosed for a separately authorized benchmark-content revision.
