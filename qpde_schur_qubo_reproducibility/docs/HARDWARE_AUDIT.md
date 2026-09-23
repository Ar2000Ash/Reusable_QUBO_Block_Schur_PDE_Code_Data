# Dirac-3 hardware audit notes

The hardware experiment is preserved as an **offline auditable record**. No
network call is needed to check the published statistics.

## Stored evidence

- `returned_samples.csv` contains 457 returned solution rows across the unique jobs.
- `unique_jobs.csv` contains the 34 distinct submitted QUBOs, job identifiers, schedules,
  sample counts, metered device usage, exact finite-bit reference states, and best returned
  states.
- `mapped_60_instances.csv` expands repeated QUBOs back to all 60 PDE inverse-column uses.
- `reconstructed_60_instances.csv` contains decoded inverse columns and the local residual
  comparisons used in the audit.
- `heat_solution.csv`, `poisson_solution.csv`, and `klein_gordon_solution.csv` contain the
  end-to-end PDE fields used in the reported analysis.
- `representative_job_request.json` documents the request structure for one representative
  24-bit problem without any account credentials.

## Headline checks

Running

```bash
python analysis/audit_dirac3.py
```

should report:

```text
Mapped inverse-column instances : 60
Unique submitted QUBOs          : 34
Mapped exact finite-bit hits    : 31/60
Unique-QUBO exact hits          : 17/34
Metered device usage           : 558 s
Stored returned unique samples : 457 rows
```

The archived job identifiers are retained for provenance. They are not credentials and do
not grant access to a QCI account.
