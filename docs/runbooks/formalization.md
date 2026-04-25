# Runbook: Formalizing a note

*Updated 2026-04-25.*

## Prerequisites

- note promoted from [blueprinting](blueprinting.md) (`lattices/xanadu/formalization/ASN-NNNN/`)
- Upstream dependencies already formalized
- Upstream summaries populated (run summarize on dependencies first)

## Steps

### 1. Formalize

```bash
python scripts/formalize.py <ASN>
```

Produces formal contracts and rewrites proofs to Dijkstra standard. Auto-commits per dependency level. Skips cached claims — delete `_cache.json` to force full re-run.

### 2. Populate the substrate

```bash
python scripts/populate-store.py
```

Imports claim, contract, and citation links from claim YAMLs into `lattices/xanadu/_store/`. Idempotent — re-run any time. Required before review/revise so the convergence predicate has data to evaluate.

### 3. Regional sweep (per-cone review)

```bash
python scripts/regional-sweep.py <ASN>
python scripts/regional-sweep.py <ASN> --cone S8    # single apex
```

Walks the dependency graph bottom-up. Reviews tightly coupled clusters as a unit. Default max 8 cycles per cone, plus a +1 confirmation review when the work loop hits the cap. Use `--cone LABEL` to target a specific apex.

### 4. Full-review (whole-ASN review)

```bash
python scripts/full-review.py <ASN>
```

Whole-ASN scan with foundation context. Catches cross-cone issues that per-cone review misses. Same predicate-driven termination as regional sweep.

### 5. Summarize

```bash
python scripts/summarize.py <ASN>
```

Populates the `summary` field in each claim YAML. Required before assembly. Hash-cached — only regenerates changed claims.

### 6. Assembly

```bash
python scripts/formalization-assembly.py <ASN>
```

Mechanical — reads YAML summaries + .md contracts, writes `formal-statements.md` and `dependency-graph.yaml` to `lattices/xanadu/manifests/`.

### 7. Individual re-runs (if needed)

```bash
python scripts/formalize.py <ASN> --dry-run         # list candidates
python scripts/formalize.py <ASN> --label T8         # single claim
python scripts/regional-sweep.py <ASN> --cone T8    # single apex review
```

---

See the [formalization guide](../guides/formalization.md) for how the V-cycle works and the [V-cycle design note](../design-notes/review-v-cycle.md) for the multi-scale architecture.
