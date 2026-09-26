# Dirac-3 signed fixed-point decoding correction

## Scope and original evidence

The hardware campaign's normalized submitted QUBO energies, reported bitstrings,
job identifiers, sample counts, and original PDE reconstructions are retained.
The archived bitstrings and Schur blocks permit independent re-decoding.

The first public archive contained a signed-decoding inconsistency: when a 12-bit
scalar had a set sign bit, some decoded numerical columns used an incorrect negative
offset. The two's-complement-like signed fixed-point rule in manuscript Eq. (17) is

```text
y = gamma * (-2^M sign + sum_{m=0}^{M-1} 2^m integer_m
             + sum_{k=1}^{K} 2^{-k} fractional_k).
```

Here B=2, M=1, K=10, so the two 12-bit segments of each 24-bit bitstring
must be decoded independently, with sign weight -2 gamma per segment.
The local residual is ||S y - e_j||_2 and the submitted, constant-free
normalized QUBO objective is (||S y - e_j||_2^2 - 1)/coefficient_scale.

## Correction findings

- The original `returned_samples.csv` had 136 of 457 rows with affected decoded
  components and residuals.
- The original `unique_jobs.csv` had 3 of 34 affected best-state rows.
- The original `reconstructed_60_instances.csv` had 10 of 60 affected
  hardware-decoded columns.
- The derived `processed/dirac_mapped.csv` had 10 of 60 affected columns.
- The `mapped_60_instances.csv` local residual fields and the normalized QUBO
  energies independently agree with the stored bitstrings and were not changed.

For example, QCI-041 has best bitstring
`010000000000111011010000` with gamma=1. Its second scalar decodes to
-0.296875, not -1.703125. The corrected local residual is approximately
0.0003019267554 rather than 1.4063060313.

The source snapshots from before this correction are preserved under
`data/provenance/pre_fix_signed_decode/`, in addition to the Git commit history.
The legacy files are included strictly for provenance and must not be used as the
current numerical results.

## Invariants

The corrected record must retain unchanged: returned and reference bitstrings,
job IDs, QCI-reported energies, independently recomputed submitted objective
values and gaps, sample multiplicities, exact-hit indicators, device timings, and
all source Schur-block entries. The corrected decoded vectors must reproduce the
stored normalized energies and their local inverse-column residuals.
The `analysis/check_dirac3_decode.py` script independently checks these invariants.

The original device service cannot be re-run offline. This correction is based on
the preserved bitstrings and analytical encoding, not a new device experiment.
