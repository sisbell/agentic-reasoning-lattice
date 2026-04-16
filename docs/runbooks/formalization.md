# Runbook: Formalizing an ASN

*Updated 2026-04-14.*

## Prerequisites

- ASN promoted from [blueprinting](blueprinting.md) (`vault/3-formalization/ASN-NNNN/`)
- Upstream dependencies already formalized
- Upstream summaries populated (run summarize on dependencies first)

## Steps

### 1. Formalize

```bash
python scripts/formalize.py <ASN>
```

Produces formal contracts and rewrites proofs to Dijkstra standard. Auto-commits per dependency level. Skips cached properties — delete `_cache.json` to force full re-run.

### 2. Property-scale review

```bash
python scripts/proof-review.py <ASN>
python scripts/contract-review.py <ASN>
```

Proof review checks logical gaps, missing cases, dependency correctness. Contract review validates contracts match proofs. Run until findings trend to zero.

### 3. Cone sweep (cluster-scale review)

```bash
python scripts/cone-sweep.py <ASN>
python scripts/cone-sweep.py <ASN> --cone S8    # single cone
```

Walks the dependency graph bottom-up. Reviews tightly coupled clusters as a unit. Default max 8 cycles per cone. Use `--cone LABEL` to target a specific apex.

### 4. Cross-review (system-scale review)

```bash
python scripts/cross-review.py <ASN>
```

Full ASN scan with foundation context. Catches carrier-set conflation, precondition chain gaps, scope mismatches.

### 5. V-Cycle (all scales composed)

```bash
python scripts/formalization-vcycle.py <ASN>
python scripts/formalization-vcycle.py <ASN> --max-passes 3
python scripts/formalization-vcycle.py <ASN> --dry-run
```

Runs the full upward-downward pass: proof → contract → cone-sweep → cross-review → cone re-check → proof re-check → contract re-check. Converged when no scale changes anything in a full pass.

### 6. Summarize

```bash
python scripts/summarize.py <ASN>
```

Populates the `summary` field in each property YAML. Required before assembly. Hash-cached — only regenerates changed properties.

### 7. Assembly

```bash
python scripts/formalization-assembly.py <ASN>
```

Mechanical — reads YAML summaries + .md contracts, writes `formal-statements.md` and `dependency-graph.yaml` to `vault/project-model/`.

### 8. Individual re-runs (if needed)

```bash
python scripts/formalize.py <ASN> --dry-run         # list candidates
python scripts/formalize.py <ASN> --label T8         # single property
python scripts/proof-review.py <ASN> --label T8      # single property review
```

---

See the [formalization guide](../guides/formalization.md) for how the V-cycle works and the [V-cycle design note](../design-notes/verification-v-cycle.md) for the multi-scale architecture.
