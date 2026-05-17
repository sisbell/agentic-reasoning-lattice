# Channel Assignment — ASN-0047 review-56

**Date:** 2026-05-16 19:48

## Issue 1: K.δ k=1 ghost-base case's reliance on T10a is formally imprecise
Reason: The pattern for "uniqueness mechanism where T10a does not formally apply" is already established in this ASN by NodeUniqueAllocation (which cites design/implementation evidence already in consultation-54). The fix is to restructure the citation following that pattern — either replace T10a with K.δ precondition + TA5 determinism, or introduce a parallel axiom. Both options are derivable from the ASN's existing axiomatic structure plus ASN-0034's foundations.

## Issue 2: T10a citation chain imprecision in cross-document disjointness derivation
Reason: Pure citation precision against ASN-0034's existing structure. T10a.2 (NonNestingSiblingPrefixes) and T10a.5 (CrossAllocatorIncomparability) are the load-bearing invariants for the same-account-sibling and different-account cases respectively. Fix is derivable from looking up ASN-0034 directly.

## Issue 3: K.δ k=1 invariant verification claimed but not explicit
Reason: Either enumerate per-invariant checks (frame-preserved or vacuous) or downgrade the load-bearing "every clause" claim. Both options use the ASN's own definitions of P0–P8, S0–S9, L0–L14, J0–J4, and the K.δ frame; no external evidence needed.

## Issue 4: K.μ~ worked example does not trace the intermediate state
Reason: Pure exposition fix — insert M_int(d) after K.μ⁻ and verify K.μ⁺ preconditions there. All values and admissibility checks are derivable from the K.μ⁻ + K.μ⁺ definitions already in the ASN.

## Issue 5: K.μ~ definition's forward-reference architecture
Reason: Structural/presentation reorganization. Choice between moving the Decomposition section earlier (with S3★-aux and CL-UNIQ as preliminaries) versus deferring K.μ~'s contract statement is an authoring decision derivable from the ASN's existing dependency structure.
