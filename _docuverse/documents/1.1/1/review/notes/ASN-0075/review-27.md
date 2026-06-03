# Review of ASN-0075

## REVISE

### Issue 1: Claims table overstates D-EXH's domain
**ASN-0075, "Claims Introduced" table, D-EXH row**: "For every reachable state Σ and every `(a, d)` ... exactly one of CURRENT, DELETED, NEVER_INCLUDED holds"
**Problem**: The lemma body restricts to composite-boundary states and explicitly warns that "At intermediate states inside a composite, P4★ may fail." This restriction is load-bearing: at an intermediate state with `a ∈ ran(M(d)) ∧ (a,d) ∉ R` (the "impossible" row, possible only because P4★ is suspended), both `CURRENT(a,d)` and `NEVER_INCLUDED(a,d)` hold, breaking *both* exhaustion and mutual exclusion. The table's "every reachable state" therefore asserts something the lemma disproves.
**Required**: Change the table entry to "every composite-boundary state" (or "every state reachable by valid composite transitions"), matching the lemma and D-BOUND.

### Issue 2: `subspace_I` misattributed to a nonexistent ASN-0036 claim
**ASN-0075, "Foundation Recap"**: "Subspace projection `subspace_I(a)` (ASN-0036, S7c): identifies the content (`s_C`) or link (`s_L`) subspace of an I-address."
**Problem**: ASN-0036 defines no claim S7c (it has S7, S7a, S7b, S7d, and `SubspaceProjection` for V-positions `subspace(v)=v₁`). The I-address projection `subspace_I(a) = E(a)₁` is defined in ASN-0047's `SubspaceConventionAxiom`. The citation points to a foundation claim that does not exist.
**Required**: Cite `subspace_I` to ASN-0047 (SubspaceConventionAxiom), where it is actually defined.

### Issue 3: Two foundation citations name claims that do not exist under those names
**ASN-0075, D-ACT**: "by SubAllocatorAxiom (e) (Disjointness, ASN-0047), `A_C(d)` is the unique content allocator..." and **D-DISCR notational convention**: "violating J0 (AllocationRequiresPlacement, ASN-0047)".
**Problem**: ASN-0047 has no "SubAllocatorAxiom" — the content sub-allocator disjointness fact (`d ≠ d' ⟹ dom(A_C(d)) ∩ dom(A_C(d')) = ∅`) lives in `SubAllocatorBundle`. And J0 is named `AllocationPlacementCoupling`, not "AllocationRequiresPlacement." Both facts are real; only the foundation labels are wrong.
**Required**: Cite `SubAllocatorBundle` for the disjointness delta and `J0 (AllocationPlacementCoupling)` for the coupling.

### Issue 4: D-SUBSP asserts a "structural necessity" without the chain it elsewhere supplies
**ASN-0075, D-SUBSP**: "'cross-document deletion of link material' is not a well-formed comparison ... no comparison document holds it as witness."
**Problem**: The ASN is meticulous elsewhere (e.g., D-EXH spells out the `L14 + S3★-aux + S3★`-contrapositive chain) but here only gestures. The actual obligation — that a link address `ℓ` with `origin(ℓ) = d_A` can never be `CURRENT(ℓ, d_B)` — requires the chain: `subspace_I(ℓ) = s_L` so `ℓ ∈ dom(L)`; CL-OWN forbids `ℓ` at a link V-position of `d_B`; L14 + S3★ content clause forbid `ℓ ∈ dom(L)` at a content V-position of `d_B`; hence `ℓ ∉ ran(M(d_B))`. Without this, "structural necessity" is asserted, not derived.
**Required**: State the explicit chain showing link addresses cannot serve as cross-document witnesses, mirroring the rigor of D-EXH.

## OUT_OF_SCOPE

### Topic 1: Restoration / "bring back this part" operation
**Why out of scope**: D-RECONS and the Composability section correctly defer restoration mechanics to a future ASN; they only note the output's form makes it possible. No revision needed.

### Topic 2: Multi-document (>2) and concurrent-snapshot generalizations
**Why out of scope**: Raised in Open Questions as future territory; not defects in the binary operation specified here.

VERDICT: REVISE
