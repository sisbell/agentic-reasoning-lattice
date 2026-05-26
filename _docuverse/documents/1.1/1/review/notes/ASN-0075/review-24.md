# Review of ASN-0075

## REVISE

### Issue 1: D-ACT bijection proof omits explicit verification of Right-maximality and Left-maximality

**ASN-0075, D-ACT, witness-run uniqueness argument**: After establishing the index-min/T1-min coincidence and the address-set correspondence, the proof concludes: "exactly the address set the inverse reconstructs from the witness run (min(C), |C|, d). The bijection is verified."

**Problem**: A witness run is a triple satisfying *four* conditions: Coverage, Origin uniformity, Right-maximality, Left-maximality. The argument verifies the address-set correspondence (which discharges Coverage; Origin uniformity follows from I-adjacency's same-origin requirement), but the bijection claim — that each equivalence class C maps to a *witness run* — also requires showing the triple `(min(C), |C|, d)` satisfies Right-maximality (`shift(min(C), |C|) ∉ deletion set`) and Left-maximality (`i_pred ∉ deletion set` when `min(C)` is not the first emission). These conditions are part of the definition of a witness run and are not implied by address-set equality alone — they assert facts about the *complement* of C in the deletion set, which the address-set argument never touches. They follow from the equivalence class's closure under I-adjacency — if `shift(min(C), |C|)` or `i_pred` were in the deletion set, they would be I-adjacent to a member of C (one shift apart, same origin by S7's shift-invariance) and therefore forced into C, contradicting either `|C| = ℓ` or `min(C)` being the index-minimum — but this argument is not in the text.

**Required**: Add explicit verification of Right-maximality and Left-maximality for each equivalence class's corresponding triple. The arguments are one sentence each, invoking the closure of equivalence classes under I-adjacency. Without these, the bijection claim is incomplete and the "uniquely determined" conclusion that anchors D-ACT's compact-form presentation rests on an unproven step.

### Issue 2: C ⊆ dom(A_C(d)) inference relies on uncited reverse direction of SubAllocatorAxiom

**ASN-0075, D-ACT proof**: "By I-adjacency's same-origin requirement, every member of C shares one origin d, so C ⊆ dom(A_C(d))."

**Problem**: The inference "shares origin d ⟹ in dom(A_C(d))" depends on the reverse direction of SubAllocatorAxiom — that every content address with origin d is allocated by A_C(d), not just that A_C(d)'s outputs have origin d. ASN-0047's SubAllocatorAxiom (a) gives the forward direction (A_C(d)'s outputs have subspace_I = s_C); SubAllocatorAxiom (e) (Disjointness) is what excludes other allocators from producing content with origin d. The reverse-direction inference is correct but the citation chain is implicit.

**Required**: Cite SubAllocatorAxiom (e) explicitly at this step, or add a one-line justification: "By SubAllocatorAxiom (e), no other allocator produces content addresses with origin d, so any content address with origin d lies in dom(A_C(d))."

VERDICT: REVISE
