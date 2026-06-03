# Review of ASN-0071

## REVISE

### Issue 1: Reinvented entity-predicate notation (IsNode / IsDocument)
**ASN-0071, Finiteness, steps (a)–(b)**: "ASN-0047 gives `E₀ = {n₀}` with `IsNode(n₀)`, so `n₀ ∉ E_doc`" and "K.δ adds `e` to `E_doc` only when `IsDocument(e)`, otherwise to `E_node` or `E_account`."
**Problem**: ASN-0047 (foundation) defines these predicates as `Node(e)`, `Account(e)`, `Document(e)` — used uniformly throughout (Σ.E stratification, K.δ, NodeBaptism, parent(e)). This ASN introduces `IsNode`/`IsDocument` for the identical predicates. Per the standing rule, an ASN must use the foundation's notation rather than reinvent it; the variant spelling forces the reader to verify the two names denote the same predicate.
**Required**: Replace `IsNode`/`IsDocument` with the foundation's `Node`/`Document` in the Finiteness section (and anywhere else they occur).

### Issue 2: `find`'s dependence on `dom(Σ.C)` mis-stated
**ASN-0071, Currency: state dependence**: "It depends only on the current state — specifically on `Σ.E_doc` and `Σ.M` (and through M's range, on `dom(Σ.C)` via S3★)."
**Problem**: This parenthetical asserts a dependence on `dom(Σ.C)`, but `find(Q)(Σ) = {d ∈ Σ.E_doc : ran(Σ.M(d)) ∩ iaddrs(Q)(Σ) ≠ ∅}` reads neither `dom(C)` nor any content value; `iaddrs` is computed purely as images of `Σ.M(d_s)`. Indeed F-CUR's own hypothesis correctly requires equality only of `E_doc` and `M`, never of `C`. The prose therefore contradicts the very claim it precedes — a careful reader could conclude that two states agreeing on `E_doc` and `M` but differing on `C` might yield different results, which F-CUR denies.
**Required**: Drop the `dom(Σ.C)` dependence clause, or restate it as mere context (S3★ guarantees `ran(M) ⊆ dom(C) ∪ dom(L)`) without implying `find` reads `C`.

## OUT_OF_SCOPE

### Topic 1: Relationship between `find`'s current-state result and provenance `R`
**Why out of scope**: The ASN correctly defers the historical-containment query (an `R`-based operation) to a future ASN and is honest that the two semantics differ; this is new territory, not an error here.

### Topic 2: Distributed-replica completeness, access-control filtering, version reconciliation as guarantee
**Why out of scope**: Each is explicitly marked under "What we do not specify" / Open Questions and belongs in a separate specification.

VERDICT: REVISE
