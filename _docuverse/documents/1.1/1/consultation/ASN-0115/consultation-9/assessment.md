# Channel Assignment — ASN-0115 review-9

**Date:** 2026-06-05 06:35

## Issue 1: R8's link sub-case describes a configuration the substrate forbids
Reason: The fix is internal. The review already supplies the formal argument from cited substrate invariants (CL-OWN, CL-UNIQ in ASN-0047) that distinct link positions cannot share an address; confining R8 to content or marking the link sub-case vacuous follows directly from those referenced per-state invariants and S5, with no design-intent or implementation evidence required.

## Issue 2: empty spec-set (`p = 0`) delivery left implicit
Reason: The fix is internal. R0's concatenation definitionally yields `⟨⟩` for the empty sequence; stating `deliver(⟨⟩, Σ) = ⟨⟩` as a successful empty delivery, parallel to R6, is derivable from the ASN's own definitions.
