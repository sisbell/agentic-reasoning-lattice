# Channel Assignment — ASN-0047 review-97

**Date:** 2026-05-18 00:43

## Issue 1: GlobalLineage proof — incorrect step count
Reason: Pure counting fix derivable from the ASN's own entity stratification (E excludes IsElement, so zeros ∈ {0,1,2} and the parent chain has at most two steps: document → account → node).

## Issue 2: J1 derivation citation in Properties table is misleading
Reason: The main text already correctly derives J1 from preserving P4 (Contains(Σ) ⊆ R) via wp, not from J0. The fix is correcting the table entry to match the existing derivation.

## Issue 3: NodeAllocationRegistry is informal but labeled "Definition"
Reason: Editorial choice between formalizing or relabeling; the open question at the end of the ASN already acknowledges the abstraction boundary is uncertain. The fix can be made from the ASN's own framing without external input.

## Issue 4: P5 and "Permanence from elementary frames" lemma are redundant
Reason: Pure consolidation of three near-duplicate predicates (lemma + P5 + P3); the fix is choosing one and citing it consistently.

## Issue 5: Link-subspace replacement asymmetry not addressed
Reason: The asymmetry follows mechanically from K.μ⁺_L's stated preconditions (ℓ ∉ ran(M(d)) first-arrangement, D-CTG★ contiguous placement) and K.λ's freshness discipline — all already in the ASN. The fix is making the consequence explicit.

## Issue 6: Forward-reference accretion and meta-prose
Reason: Pure editorial cleanup — strip meta-prose and presentational commentary without adding new content.

## Issue 7: S4 cross-document distinctness for K.δ on documents lacks explicit lemma citation
Reason: The Cross-document disjointness chain lemma is already proved in the ASN; the fix is extending its citation to cover K.δ events at the account level (the structural argument is identical to the content/link case).

## Issue 8: SubAllocatorAxiom activation timing relative to T10a's spawnPt premise
Reason: The ASN already acknowledges the anchors lie outside T10a-tracked domains; the fix is adding one sentence noting the bypass and citing SC-NEQ at the anchor level. T10a's structure is in ASN-0034 and the consequence is derivable.

## Issue 9: K.μ⁻ exhaustiveness lemma — proof of mutual exclusion of cases (b) and (c)
Reason: Pure proof tightening — the disjointness already follows from the case-split structure, so the fix is removing the redundant closing argument.

## Issue 10: Initial state and base case at Σ₀ — bootstrap node baptism event not characterized
Reason: Editorial clarification — adding one sentence stating that n₀ is established by system genesis rather than by a K.δ event, scoping NodeUniqueAllocation to subsequent allocations.

## Issue 11: P3 versus L12 — labeling and coverage
Reason: Pure consolidation choice between dropping L12 (as subsumed by P3) or dropping P3 (citing the four foundation invariants separately). Either choice is internal.
