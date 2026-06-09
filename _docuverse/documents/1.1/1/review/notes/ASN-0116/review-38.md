# Review of ASN-0116

## REVISE

### Issue 1: Clause-1 freshness discharge omits the first-emission branch

**ASN-0116, "INSERT as a valid composite over the K-vocabulary," K.α step**: "Each commits one fresh content address along A_C(d); the k-th acts on a store already holding `{shift(a, 0), …, shift(a, k−1)}`, against which **SubsequentEmissionFreshness** gives `shift(a, k) ∉ dom(C) ∪ dom(L)`."

**Problem**: This blanket citation is wrong for the first allocation (`k = 0`) when `d`'s content region is initially empty — i.e. when `{a' ∈ dom(C) : origin(a') = d} = ∅`. In that case `a = shift(a, 0) = [d.0.s_C.1]` is a **first** emission, and SubsequentEmissionFreshness is *inapplicable*: its precondition is precisely the subsequent-emit predicate `{a' ∈ dom(C) : origin(a') = d} ≠ ∅`, which fails. Freshness there is discharged by **FirstEmissionFreshness**, not SubsequentEmissionFreshness. This is exactly the boundary the ASN itself exercises: the `ValidFirstInsertionPosition` precondition path and the "empty subspace" worked boundary are the first-content-into-`d` case. (Note the prose in "What is allocated" *does* split both branches for the start address `a` — "FirstEmissionFreshness (when d's content region is empty) and SubsequentEmissionFreshness (otherwise)" — but the formal clause-1 discharge, which is what establishes the composite's validity, does not.) Since validity is the gate for the appeal to ExtendedReachableStateInvariants, the omitted branch leaves clause 1 unproven on a reachable, in-scope case.

**Required**: In the K.α step of the composite verification, split `k = 0` (FirstEmissionFreshness when `{a' ∈ dom(C) : origin(a') = d} = ∅`, SubsequentEmissionFreshness otherwise) from `k ≥ 1` (always SubsequentEmissionFreshness, since the prior in-insert allocation makes the region non-empty). The empty-subspace worked example, which silently carries the `[d.0.s_C.7]` start address from the prior (non-empty) scenario, should also note the first-emission start address `[d.0.s_C.1]` to exercise the branch.

## OUT_OF_SCOPE

### Topic 1: Insertion at a transcluded/shared position
The first Open Question (insertion at a position shared by transclusion) is correctly deferred — transclusion is ASN-0118 territory, and IP5 already handles the simpler shared-I-address-via-distinct-arrangements case.

### Topic 2: Concurrent freshness without a serializing authority
The second Open Question (two concurrent insertions claiming freshness) belongs to a concurrency/baptismal-authority ASN, not here; INSERT correctly assumes the sequential transition model (SequentialTransitionAxiom).

---

Remarks not rising to REVISE: the identity-permanent/arrangement-ephemeral motif recurs across the intro, the allocation section, IP3, and the seam discussion, but each instance does locally distinct work, so it is not duplication. The I3-family citations for F-SUB/F-DOC/I-SHIFT/I-LEFT are loose (the rigorous chain for cross-subspace/cross-document invariance runs through the composite's own K.μ⁻ full-link-retention and K.μ⁺ content-restriction, which the note in fact states in the composite section), but the results hold and the mechanism is present — adequate given ASN-0082's foundation status.

VERDICT: REVISE
