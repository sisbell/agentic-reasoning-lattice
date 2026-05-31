# Review of ASN-0093

## REVISE

### Issue 1: Intro undercounts the substrate's new content-side invariants — C2 is omitted

**ASN-0093, opening paragraph**: "The substrate adds three content-side invariants that the inherited models do not carry — C1b (content element-field depth), the C-clause of L0 (content subspace partition), and C1c (content allocator conformance) — proved within this note."

**Problem**: The Properties Introduced table marks **C2 (ContentScopedAllocation)** as a substrate-added content-side invariant — Source "Substrate; content-side analog of L1a" — not as a restatement of an inherited ASN-0036 invariant (contrast C0 "restated from ASN-0036 S0/S1" and C1 "restated from ASN-0036 S7b"). C2's claim `origin(a) ∈ dom(M)` is genuinely new: ASN-0036's S7a is an attribution claim, not a `dom(M)`-membership invariant, and `dom(M)` as "allocated documents" is introduced by this substrate. So C2 is a content-side invariant the inherited models do not carry, yet the intro's enumeration — which reads as an exhaustive accounting of new content-side invariants — drops it. The count "three" mismatches the table's four newly-added content-side items (C1b, C1c, C2, plus the L0 C-clause).

**Required**: Add C2 to the intro enumeration (and adjust the count), or, if C2 is intended to be read as inherited from ASN-0036 S7a, change its table Source to a "restated from ASN-0036 S7a" form so the intro and table agree.

### Issue 2: C1c/L1c subsequent-emit chain exhibition carries freshness prose that is not part of the allocator-conformance claim

**ASN-0093, *C1c chain exhibition*, subsequent-emit case**: "Within-chain freshness against the rest of `A_C(d)`'s chain is discharged by ChainEnumerationInjectivity applied to `(a_prev, a)`, with both indices established to inhabit `A_C(d)` by ChainMembershipForOrigin ... ; cross-document collisions with other documents' content chains are ruled out by the Cross-document disjointness lemma." (and the L1c parallel: "the same ... citations discharge per-step admissibility, **freshness**, and the strengthened clauses")

**Problem**: C1c (ContentAllocatorConformance) and L1c are pure *existence* claims — "every content/link address has a T10a-conforming step sequence from its home document." Neither asserts that the address is distinct from any other address. The freshness/cross-document-collision sentence establishes `a ∉ dom(C) ∪ dom(L)`, which is the obligation of SubsequentEmissionFreshness (consumed by the K.α/K.λ binding precondition and the SD discharge), not of C1c/L1c. The conforming chain exists whether or not `a` collides with anything. This is freshness content relocated into the conformance discharge — prose that does not advance the C1c/L1c existence argument and duplicates SubsequentEmissionFreshness.

**Required**: Strike the within-chain/cross-document freshness sentences from the C1c and L1c subsequent-emit chain exhibitions, leaving only per-step admissibility (TA5a/TA5(c)), the chain-extension construction, and the strengthened clauses (`k₁ = 2`, `#tᵢ > #origin`). Freshness is already carried by SubsequentEmissionFreshness.

## OUT_OF_SCOPE

### Topic 1: Concurrent emission discipline across allocators
**Why out of scope**: The substrate commits to SequentialTransitionAxiom; the coordination discipline for concurrent allocators is correctly listed as an Open Question for a higher layer, not a gap in this note.

VERDICT: REVISE
