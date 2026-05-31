# Review of ASN-0093

## REVISE

### Issue 1: Editorial comparison to L14 does not advance the SD derivation (and is misleading here)
**ASN-0093, SD (StoreDisjointness)**: "SD is thereby strictly stronger than ASN-0043's L14 (DualPrimitive), whose disjointness clause is the `s_C`-sliced `dom(L) ∩ dom(C)|_{s_C} = ∅`."
**Problem**: The SD derivation completes at "the domains are disjoint." This trailing clause is a use-comparison against a foundation invariant that adds no step to the proof. Worse, it is inaccurate *in this substrate*: L0's C-clause forces every content address into `s_C`, so `dom(C) = dom(C)|_{s_C}` and SD coincides with the sliced L14 — it is not "strictly stronger" here.
**Required**: Delete the comparison, or if the relationship is worth recording, state it accurately (the two coincide under L0's C-clause).

### Issue 2: Editorial tag appended to the Cross-document disjointness conclusion
**ASN-0093, Cross-document disjointness lemma**: "…and T10 gives `a ≠ b` for any `a` extending `p₁`, `b` extending `p₂` — the strictly stronger any-extension claim."
**Problem**: The conclusion already states the any-extension claim (`a ≠ b` for all extensions). The dangling "— the strictly stronger any-extension claim" is self-commentary that restates what was just proved.
**Required**: Remove the trailing clause.

### Issue 3: Base-case use-site inventory with defensive justification
**ASN-0093, Base case verification**: "(the chain-indexed ASN-0040 disciplines — ChainElementT4Validity, ChainEnumerationInjectivity, ChainUniformZeroCount, DisjointSubAllocatorChains — hold regardless, being state-independent citations)."
**Problem**: The base case is discharged by "all stores empty ⟹ vacuous." This parenthetical enumerates four named disciplines and adds a defensive "hold regardless, being state-independent" rationale — exactly the use-site-inventory-plus-justification pattern the anti-bloat pass targets. It does not advance the base case.
**Required**: Drop the parenthetical; the disciplines' state-independence is already implicit in their not being state-quantified.

### Issue 4: Redundant elaboration of "atomic" in SequentialTransitionAxiom
**ASN-0093, SequentialTransitionAxiom**: "…atomic, uninterruptible, and totally ordered: each transition evaluates its precondition against `Σ` and commits its effect to `Σ'` in one indivisible step, with no intermediate state in which a transition has begun but not committed."
**Problem**: "with no intermediate state in which a transition has begun but not committed" restates "atomic/indivisible" in different words (pattern: two clauses saying the same thing). The earlier "one indivisible step" already carries it.
**Required**: Keep one formulation of atomicity; drop the restatement.

## OUT_OF_SCOPE

### Topic 1: K.σ admits any T4-valid `zeros=2` document without T10a-conformance
**Why out of scope**: K.σ's precondition pins only `T4-valid(d) ∧ zeros(d) = 2 ∧ d ∉ dom(M)`, not that `d` is a GlobalUniqueness/T10a allocator output (ASN-0036 S7d). The cross-document disjointness lemma is sound regardless (it needs only M0 and prefix relations on the *anchors*), so this is not an error here — whether document allocation must itself be allocator-conforming belongs to a document-allocation-discipline layer, not the substrate.

### Topic 2: Sub-allocator stratification for `s ≥ 3`
**Why out of scope**: Already listed as an Open Question; the substrate commits to exactly two subspaces (content, link) and that suffices for its stated invariants.

VERDICT: REVISE
