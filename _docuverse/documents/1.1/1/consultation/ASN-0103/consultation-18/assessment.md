# Channel Assignment — ASN-0103 review-18

**Date:** 2026-06-05 02:16

## Issue 1: ActivatedEmission for the new document `d` is asserted, not discharged
Reason: Closing the hole requires knowing whether an account, the moment it exists, is meant to (and does) carry an activated document sub-allocator. Nelson grounds the design assumption (option a); Gregory confirms whether the implementation establishes this on account creation (the account-level analogue of SubAllocatorBundle, option b).
Nelson question: Is an account intended to support document creation beneath it the instant it exists — i.e. does account provisioning conceptually carry, as a built-in guarantee, an available document sub-allocator with no separate activation step?
Gregory question: When the implementation creates an account, does it activate/initialize that account's document sub-allocator (so the first CREATENEWDOCUMENT draws from an already-live allocator), or is the document allocator brought into being only at first document creation?

## Issue 2: GlobalUniqueness invoked with an undischarged T10a-conformance premise, where B7 already suffices
Reason: Internal — the ASN already cites B7 (NamespaceDisjointness, ASN-0040) for version distinctness; cross-account distinctness follows the same way from `(A,2) ≠ (A',2)`, so the fix is to substitute B7 for the GlobalUniqueness appeal using machinery already present.

## Issue 3: Ownership precondition mis-cited to O5
Reason: Internal — CND.own already performs the correct O1 (PrefixDetermination) transitivity derivation; the fix is to cite O1 for the ownership predicate and reserve O5 (SubdivisionAuthority) for the allocation-authorization step, derivable from the ASN's own content.
