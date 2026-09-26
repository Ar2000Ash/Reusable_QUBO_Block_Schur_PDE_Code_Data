# QCI hardware provenance and reconstructed polynomial inputs

This directory preserves the original QCI source-level evidence recovered on 2026-09-26, together with independently regenerated *mathematical* QUBO inputs and corrected offline postprocessing. The complete recovery ZIP is kept in nine immutable binary pieces solely for transport inside Git. Reassemble and verify it from the project directory:

```sh
python analysis/verify_qci_recovery.py
```

The script verifies each part's Git blob hash, reconstructs a 394421-byte ZIP with SHA-256 `2cfd274f76e0302570042a6ed071cfc0bcc18906f03c30e56a85554cddf4a3a1`, checks the package manifest, regenerates all QUBO inputs and derived CSVs offline, reruns the independent numerical audit and checks snapshot integrity. It never uses vendor credentials.

Original, immutable source evidence: six author-supplied preprocessing CSV files and the original complete `qci_hardware_results_bundle_4.zip`, including `qci_hardware_raw_results.jsonl` with 34 completed saved device responses, returned states, job-submission metadata, polynomial file IDs and counts. The 457 distinct returned sample states represent a combined multiplicity of 840. Legacy original CSVs are preserved unmodified and explicitly labelled `UNCORRECTED`.

Derived outputs: 34 mathematically reconstructed 24-bit normalized QUBOs (300 full upper-triangular terms each), the 60-to-34 reuse mapping, source normalization and nonpruning checks, independent energy audit, correctly signed fixed-point decoded samples, reconstructed best state and per-PDE aggregates. Reconstructed term filenames begin with `RECONSTRUCTED_` and preserve historical original filenames and hashes *separately* in the manifest.

**Limitations:** All 34 reconstructed CSV SHA-256 values differ from their historical term-file hashes, even though the mathematical coefficients reproduce the stored full-precision objectives. The original byte-for-byte vendor polynomial uploads and original authenticated upload client are not recovered. The original exhaustive 24-bit enumeration driver and full PDE cached-factor reconstruction driver also remain missing. No new QCI run was performed. Exact-hit statements refer to the preserved archived reference bitstrings and verified returned-state matching, not to an independently re-run exhaustive proof.

The archived recovery package includes its own README, audit report, source tables, raw hardware JSONL, reconstruction and verification scripts, 34 explicit coefficient files, corrected results, and checksum inventory. The original paper's PDE solution fields and figures live in the companion main repository, not in the recovered local-QUBO package.
