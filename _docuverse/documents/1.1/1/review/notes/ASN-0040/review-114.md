# Review of ASN-0040

## REVISE

### Issue 1: B7 preamble is defensive meta-prose
**ASN-0040, B7 (Namespace Disjointness)**: "We cannot simply invoke them, because B7 quantifies over *every* B6-valid pair `(p, d)` with arbitrary `p ∈ T`... A reduction would require first exhibiting, for each such `(p, d)`, a conforming allocator whose domain is exactly S(p, d), and then ruling out the aliasing collision... We therefore re-derive disjointness directly..."
**Problem**: This is the forward-reference-accretion pattern — prose explaining *why the proof takes its approach* (and why it does not reduce to the foundation) rather than advancing the disjointness argument. The reader must skip a paragraph of defense to reach the actual case analysis. The load-bearing content is a single fact: B7 quantifies over all B6-valid pairs, not only allocator-tree allocators, so it is proved directly.
**Required**: Compress to one sentence stating that disjointness is derived directly from the canonical stream form because B7 ranges over all B6-valid pairs. Drop the hypothetical reduction sketch.

### Issue 2: B0a-frame enumerates its downstream consumers
**ASN-0040, B0a-frame (Frame Preservation)**: "The invariants B1, B10, and B_fin are each of this form (predicates on s.B), so each inherits frame preservation from B0a-frame."
**Problem**: Use-site inventory. The proofs of B1, B10, and B_fin already each cite "discharged by B0a-frame" at their frame case; this sentence restates that list a second time at the lemma's definition site. Such inventories rot as invariants are added or removed, and duplicate the per-proof citations.
**Required**: Delete the enumerating sentence. State the corollary (frame ops preserve any `φ(s.B)` predicate) and let each invariant proof cite it where used. Likewise trim "the s.B-frame case is discharged here once and for all; only the baptismal case requires per-invariant treatment" to the bare lemma.

### Issue 3: forward-pointer parenthetical in S(p,d)
**ASN-0040, S(p,d) (SiblingStream)**: "We establish this canonical form and the uniform length #cₙ = #p + d by induction (the strict ordering is proved separately at S0 below)."
**Problem**: Document-ordering parenthetical that does not advance the canonical-form derivation. S0 follows immediately and stands on its own.
**Required**: Remove the parenthetical.

## OUT_OF_SCOPE

None. The Open Questions correctly defer ownership, the parent-prerequisite chain, allocator/registry alignment (`allocated(s) ⊆ s.B`), seed admissibility, bulk allocation, cross-replica ordering, and per-subspace contiguity to future ASNs.

(Verification notes: the B6 sufficiency/necessity split is sound and matches TA5a's `k=1∧zeros≤3` / `k=2∧zeros≤2` boundaries; the B7 case analysis is exhaustive — length split, equal-length parents via T3, unequal-length parents via T4's nonzero-last-component — and each disagreement is correctly shown to sit at a fixed invariant-prefix position in both streams; B8 Case 1's →*-ordering argument and the freshness/B1/B10/B_fin inductions are rigorous; the Step 1–6 trace exercises both d=1 and d=2 at the saturated-budget boundaries. These check out.)

VERDICT: REVISE
