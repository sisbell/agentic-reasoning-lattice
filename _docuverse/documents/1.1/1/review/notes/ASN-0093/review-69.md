# Review of ASN-0093

## REVISE

### Issue 1: Freshness proof-pointers embedded in the K.α / K.λ binding preconditions
**ASN-0093, K.α (ContentAllocation), binding precondition**: "*First emission* … `a = [d.0.s_C.1]`. Freshness against `dom(C) ∪ dom(L)` is supplied by FirstEmissionFreshness." and "*Subsequent emission* … Freshness of `a` against `dom(C) ∪ dom(L)` is supplied by SubsequentEmissionFreshness (the within-document / cross-document / cross-subspace split, above)." (identically in K.λ).
**Problem**: A precondition states what must hold for the transition to fire. Freshness is not a checkable requirement on the caller — it is a *derived consequence* of the address-selection rule plus the standing invariants, established by the named lemmas and consumed in the C0/append-only discharge. The "Freshness … is supplied by X" sentences are proof-pointers occupying a precondition slot, and the parenthetical "(the within-document / cross-document / cross-subspace split, above)" is a structural reminder of the lemma's internal shape that adds nothing to the selection rule. This is proof/essay content in a structural slot — flag the placement.
**Required**: Reduce each branch's precondition to the selection rule (the first-emit/subsequent-emit predicate and the resulting address form). State freshness once, where it is used — in the discharge of C0/append-only (and the ChainMembershipForOrigin extension) — not in the precondition.

### Issue 2: Properties Introduced table reproduces lemma premise lists in the Source column
**ASN-0093, Properties Introduced table**: e.g. "ChainDiscipline | … | Premises: ASN-0040 SiblingStream; B6-validity of each parent `(b_·(d), 1)`; the K.α/K.λ emission rules." and similarly FirstEmission, ChainMembershipForOrigin, Cross-doc disjointness.
**Problem**: For the derived lemmas the Source column has grown from a terse origin pointer into a second copy of the premise list already given in each lemma body. An index that re-inventories dependencies is the use-site-inventory accretion pattern the note's classifier targets; the premise prose now lives in two places and will drift.
**Required**: Collapse the Source column to a one-token origin pointer (e.g., "Substrate" or the single governing ASN-0040 result); let the lemma bodies carry the premise lists.

## OUT_OF_SCOPE

### Topic 1: Concurrency discipline for parallel allocators
**Why out of scope**: Already correctly deferred in Open Questions; the substrate commits to atomic/sequential transitions (SequentialTransitionAxiom), and a multi-allocator concurrency protocol is new territory for a higher-layer ASN, not a defect here.

### Topic 2: Sub-allocator stratification for subspace identifiers `s ≥ 3`
**Why out of scope**: The substrate axiomatically fixes exactly two subspaces (`s_C = 1`, `s_L = 2`); coordinating a third sub-allocator is a future extension, not an omission in this note.

VERDICT: REVISE
