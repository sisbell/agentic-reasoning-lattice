# Runbook: Claim convergence on a note

*Updated 2026-04-25.*

## Prerequisites

- note promoted from [claim derivation](claim-derivation.md) (`lattices/xanadu/claim-convergence/ASN-NNNN/`)
- Upstream dependencies already converged
- Upstream summaries populated (run summarize on dependencies first)

## Steps

### 1. Converge

```bash
python scripts/converge.py <ASN>
```

Produces formal contracts and rewrites proofs to Dijkstra standard. Auto-commits per dependency level. Skips cached claims — delete `_cache.json` to force full re-run.

### 2. Populate the substrate

```bash
python scripts/migration_tools/populate-store.py
```

Imports claim, contract, and citation links from claim YAMLs into `lattices/xanadu/_docuverse/`. Idempotent — re-run any time. Required before review/revise so the convergence predicate has data to evaluate.

### 3. Cone sweep (per-cone review)

```bash
python scripts/claim-cone-sweep.py <ASN>
python scripts/claim-cone-sweep.py <ASN> --cone S8    # single apex
```

Walks the dependency graph bottom-up. Reviews tightly coupled clusters as a unit. Default max 8 cycles per cone, plus a +1 confirmation review when the work loop hits the cap. Use `--cone LABEL` to target a specific apex.

### 4. Full-review (whole-ASN review)

```bash
python scripts/claim-full-review.py <ASN>
```

Whole-ASN scan with foundation context. Catches cross-cone issues that per-cone review misses. Same predicate-driven termination as cone sweep.

### 5. Summarize

```bash
python scripts/summarize.py <ASN>
```

Populates the `summary` field in each claim YAML. Required before assembly. Hash-cached — only regenerates changed claims.

### 6. Assembly

```bash
python scripts/claim-assembly.py <ASN>
```

Mechanical — reads YAML summaries + .md contracts, writes `formal-statements.md` and `dependency-graph.yaml` to `lattices/xanadu/manifests/`.

### 7. Individual re-runs (if needed)

```bash
python scripts/converge.py <ASN> --dry-run         # list candidates
python scripts/converge.py <ASN> --label T8         # single claim
python scripts/claim-cone-sweep.py <ASN> --cone T8    # single apex review
```

## Querying the link graph

The substrate at `lattices/xanadu/_docuverse/` carries the protocol's runtime
state — claims, contracts, citations, comments, resolutions. The
convergence predicate evaluates over this graph; the orchestrators
consume it; operators can query it directly for inspection.

```python
import sys; sys.path.insert(0, "scripts")
from lib.store.store import Store
from lib.store.queries import (
    is_converged, is_claim_converged, is_asn_converged,
    unresolved_revise_comments, all_claim_paths, current_contract_kind,
)

s = Store()
```

**Common queries:**

```python
# Lattice-wide convergence
is_converged(s)

# Per-claim
is_claim_converged(s, "lattices/xanadu/claim-convergence/ASN-0034/T3.md")

# Per-ASN
is_asn_converged(s, "ASN-0034")

# All open revise comments (across the lattice)
unresolved_revise_comments(s)

# Open revise comments for one claim
unresolved_revise_comments(s, "lattices/xanadu/claim-convergence/ASN-0034/T3.md")

# Every claim path the lattice knows about
all_claim_paths(s)

# Contract kind for a claim (e.g., "axiom", "theorem")
current_contract_kind(s, "lattices/xanadu/claim-convergence/ASN-0034/T0.md")
```

**Lower-level primitives** (Xanadu-aligned):

```python
# Find all citations from a claim
s.find_links(
    from_set=["lattices/xanadu/claim-convergence/ASN-0034/T3.md"],
    type_set=["citation"],
)

# Find all reviews
s.find_links(type_set=["review"])

# Count comments on a claim
s.find_num_links(
    to_set=["lattices/xanadu/claim-convergence/ASN-0034/T3.md"],
    type_set=["comment"],
)
```

**Inspecting JSONL directly:**

```bash
# How many links of each type?
jq -r '.type_set[0]' lattices/xanadu/_docuverse/links.jsonl | sort | uniq -c

# Find any link by content match
grep "T3.md" lattices/xanadu/_docuverse/links.jsonl | jq .
```

The SQLite index at `lattices/xanadu/_docuverse/index.db` is rebuildable
from JSONL via `Store().rebuild_index()`. The JSONL is the source of
truth and is git-versioned alongside the lattice.

---

See the [Claim Convergence Protocol](../protocols/claim-convergence-protocol.md) for the predicate contract and stage-1 architecture.
