# Channel Assignment — ASN-0070 review-46

**Date:** 2026-06-03 00:23

## Issue 1: M-int cited with a precondition it does not supply
Reason: The fix is a proof-structure correction internal to the ASN — restrict the quantifier to `V(β) ⊆ dom(M(d))` via B3 (Consistency, ASN-0058) before applying M-int. Both B3 and M-int are already cited in the note and the review states the discharge step explicitly; no design intent or implementation evidence is required.

## Issue 2: Verbatim coverage-membership caveat repeated across worked configurations
Reason: This is an editorial anti-bloat fix — factor the depth-`m_a` reduction into a single remark and cite it per configuration. The structural fact is already established in the note's own content; no external channel is needed.
