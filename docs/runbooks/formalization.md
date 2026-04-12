# Runbook: Formalizing an ASN

*Updated 2026-04-12.*

## Prerequisites

- ASN promoted from [blueprinting](blueprinting.md) (`vault/3-formalization/ASN-NNNN/`)
- Upstream dependencies already formalized

## Steps

### 1. Formalize

```bash
python scripts/formalize.py <ASN>
```

Produces formal contracts and rewrites proofs to Dijkstra standard. Auto-commits per dependency level. Skips cached properties — delete `_cache.json` to force full re-run.

### 2. Review cycle

```bash
python scripts/formalization-review.py <ASN>
```

Runs proof review → contract review → cross-review → dependency review in a convergence loop. Watch for convergence: the number of properties being changed should trend toward zero. Once converged, flush the cache (`rm _cache.json`) and run again — a clean re-run that converges quickly confirms the ASN is stable.

### 3. Assembly

```bash
python scripts/formalization-assembly.py <ASN>
```

Produces `formal-statements.md` and `dependency-graph.yaml` in `vault/project-model/`.

### 4. Individual re-runs (if needed)

```bash
python scripts/formalize.py <ASN> --dry-run         # list candidates
python scripts/formalize.py <ASN> --label T8         # single property
python scripts/proof-review.py <ASN>                 # fix proof gaps
python scripts/contract-review.py <ASN>              # fix contract mismatches
python scripts/cross-review.py <ASN>                 # structural analysis
python scripts/proof-review.py <ASN> --label T8      # single property review
```

---

See the [formalization guide](../guides/formalization.md) for how the pipeline works, caching, dependency management, and design decisions.
