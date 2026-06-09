# Channel Assignment — ASN-0118 review-4

**Date:** 2026-06-08 21:50

## Issue 1: CP8 invokes P4★, a composite-boundary property, but the standing precondition only licenses per-state invariants
Reason: This is a proof-scoping fix internal to the ASN's own formal apparatus. Both options the reviewer offers — re-scoping the standing precondition to assert a composite boundary, or re-grounding the inference in a per-state invariant — are decidable from ASN-0047's already-cited invariant taxonomy and the sequential-transition model the ASN builds on. No design intent or implementation evidence is at stake; it is bookkeeping over properties the ASN already references.

## Issue 2: The ValidComposite argument discharges J1★ and J1'★ but is silent on J0
Reason: The reviewer supplies the entire fix — J0 is vacuous because CP1 makes `dom(C') ∖ dom(C) = ∅`, so its universal quantifier is empty. This follows directly from CP1, already proven in the ASN, and ValidComposite's J0 definition from ASN-0047. Fully derivable internally.
