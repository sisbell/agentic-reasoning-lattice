# Review of ASN-0076

## REVISE

### Issue 1: L12 mis-classified as per-state invariant
**ASN-0076, "Invariant inheritance" paragraph (end of E0)**: "by ExtendedReachableStateInvariants (ASN-0047) every per-state invariant of the extended reachable state continues to hold at the post-state — in particular L0, L1, L1a, L1b, L1c, L3, L12, L14, L-fin, CL-OWN, CL-UNIQ..."
**Problem**: L12 is not in ASN-0047's ExtendedReachableStateInvariants list. L12 is structurally a transition invariant (it quantifies over `Σ → Σ'`) and appears in ASN-0047's ExtendedTransitionInvariants as part of P3 = P0 ∧ P1 ∧ P2 ∧ L12. Citing it via ExtendedReachableStateInvariants is incorrect.
**Required**: Cite L12's preservation via ExtendedTransitionInvariants (P3), separately from the per-state inheritance. E1's direct invocation of L12 already does the right thing — only the inheritance paragraph needs adjustment.

### Issue 2: S0/S1 mis-classified in "S-invariants S0–S3★"
**ASN-0076, same paragraph**: "and the S-invariants S0–S3★, S7a–d, S8a, S8-fin, S8-depth, S8★..."
**Problem**: The range "S0–S3★" sweeps in S0 (ContentImmutability, a transition-level axiom in ASN-0036) and S1 (StoreMonotonicity, derived from S0 across transitions). Neither is in ExtendedReachableStateInvariants; both are subsumed by P0 in ExtendedTransitionInvariants. The per-state list begins at S2.
**Required**: Either narrow the range to "S2, S3★, S3★-aux, S4" or split the citation so S0/S1 are inherited via P0 (ExtendedTransitionInvariants) and S2 onward via ExtendedReachableStateInvariants.

### Issue 3: Implicit step in content-disjointness discharge
**ASN-0076, E0 successor sub-case (b)**: "By SubAllocatorAxiom.Disjointness, dom(A_L(d_new)) is disjoint from every content sub-allocator's domain; combined with L14 (StoreDisjointness, ASN-0047), ℓ_new ∉ dom(Σ.C)."
**Problem**: L14 says `dom(Σ.L) ∩ dom(Σ.C) = ∅`. To conclude `ℓ_new ∉ dom(C)` from L14, one needs `ℓ_new ∈ dom(L)` — but at this precondition check ℓ_new is not yet in dom(L). The alternative chain via Disjointness requires the unstated inclusion `dom(Σ.C) ⊆ ∪_d dom(A_C(d))`. The same elision recurs in the supersession step.
**Required**: Either (a) make the inclusion `dom(Σ.C) ⊆ ∪_d dom(A_C(d))` explicit (derived from K.α's allocator-routed semantics and P6), or (b) replace with the direct subspace argument: SubAllocatorAxiom.Subspace gives `subspace_I(ℓ_new) = s_L`; L0 gives `subspace_I(a) = s_C` for `a ∈ dom(C)`; SC-NEQ gives `s_C ≠ s_L`; hence `ℓ_new ∉ dom(C)`.

## OUT_OF_SCOPE

### Topic 1: τ_sup convention and supersession-type recognition
**Why out of scope**: The ASN explicitly defers the convention pinning `τ_sup` to a designated supersession-type address. This belongs in a future ASN on type-endset conventions, not in EDITLINK. The structural separation (E4 establishes spans-in-endsets; semantic identification deferred) is rigorous.

### Topic 2: Chains of supersession, cycles, multi-link supersession, retraction semantics, discovery operations, content/link edit interaction
**Why out of scope**: Each is acknowledged in the Open Questions list. They presuppose machinery (chain-walking, type-endset recognition, reader policies) that EDITLINK alone is not the right site to specify.

VERDICT: REVISE
