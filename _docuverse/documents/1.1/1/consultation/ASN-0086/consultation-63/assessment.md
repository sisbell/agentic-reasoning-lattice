# Channel Assignment — ASN-0086 review-63

**Date:** 2026-05-19 11:30

## Issue 1: R0 subsequent-emission freshness argument is incomplete
Reason: The proof needs to discharge three collision sources for K.λ's freshness precondition. The author needs to know which specific ASN-0093 lemmas (if any) deliver cross-allocator disjointness, or whether the cleanest fix is a holistic appeal to K.λ's freshness postcondition. This is evidence about ASN-0093's contents.
Gregory question: Does ASN-0093 provide a named lemma (e.g., DisjointSubAllocatorChains, CrossDocDisjointness) that delivers `inc(ℓ_prev, 0)` distinctness against `dom(L)` elements homed at d' ≠ d, or is cross-home freshness derivable only as a postcondition of K.λ's contract (via the L1a NUDE-prefix projection plus ChainPrefixExtension)?

## Issue 2: R7a iteration ordering argument is under-elaborated
Reason: The fix is to cite R0a-Cor1 (proved within this ASN) for chain-order existence per home, and to note K.λ's origin-scoped homed-set predicate (already stated in the ASN's transition-relation definition) for per-home determinism. Both citations are derivable from material already in ASN-0086.

## Issue 3: R0a-Cor2 zero-position stability not fully derived
Reason: The bridge to position-stability requires ChainPrefixExtension (or TA5(c) + TA5-SigValid), both of which are already cited elsewhere in ASN-0086. The fix is purely an internal proof elaboration adding the already-available lemma to R0a-Cor2's argument.

## Issue 4: Worked sketch's invocation of R6c-Corollary overreaches the corollary's stated conclusion
Reason: The fix is editorial — either cite L12 + L12a directly (already cited multiple times in this ASN) for pointwise `A_K` preservation, or split R6c-Corollary's claim to expose the broader stability result already established within its proof. Fully internal to the ASN.
