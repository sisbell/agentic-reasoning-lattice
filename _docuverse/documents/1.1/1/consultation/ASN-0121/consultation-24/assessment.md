# Channel Assignment — ASN-0121 review-24

**Date:** 2026-06-09 02:45

## Issue 1: FL-WILD table overclaims "consulting no endset" for the all-wildcard operation
Reason: The fix is internal — the ASN already establishes that `addressable(Σ) = dom(Σ.L) \ nullified(Σ)` and that computing `nullified` reads slot-3 endsets and retraction to-coverages (FL-DEC, FL-DEF). Scoping the "consulting no endset" clause to `sat` versus the whole operation is a precision edit derivable from the ASN's own definitions; no design-intent or implementation evidence is required.
