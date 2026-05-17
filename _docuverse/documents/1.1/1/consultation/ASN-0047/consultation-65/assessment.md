# Channel Assignment — ASN-0047 review-65

**Date:** 2026-05-17 00:37

## Issue 1: Cross-document disjointness chain proof gap (version pairs not covered)
Reason: Fix is derivable from the ASN — the K.δ k=1 versioning case is already defined here, and the structural divergence at position #d₁+1 (zero separator vs. positive version increment) follows from TA5 and Prefix in ASN-0034.

## Issue 2: K.μ⁻ exhaustiveness lemma's mutual exclusion claim is incorrect
Reason: Pure logic issue — the lemma's case definitions need to match what the partition algorithm actually does (adding a contiguity clause to case (c) or refactoring (b)/(c) to be definitionally disjoint). Internal to the proof.

## Issue 3: S4 derivation for K.λ first-link case incorrectly invokes T10a
Reason: The K.λ definition in the ASN already establishes that SubAllocatorAxiom (not T10a) underwrites first-link freshness; the S4 derivation must be rewritten to match this existing internal commitment.

## Issue 4: "S8-scope in the extended state" note attributes link-subspace decomposition to wrong invariants
Reason: Misattribution — the K.μ⁺_L section in the ASN already cites the correct invariants (D-CTG★, D-MIN★, S8-fin, S8-depth, S8a); the S8-scope note just needs to use the same citations.
