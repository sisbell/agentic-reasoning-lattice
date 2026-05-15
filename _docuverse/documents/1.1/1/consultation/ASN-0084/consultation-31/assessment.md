# Channel Assignment — ASN-0084 review-31

**Date:** 2026-05-15 13:30

## Issue 1: Helper lemma involution claim unjustified
Reason: The fix is derivable from the ASN alone. The review specifies exactly which foundation lemmas (NAT-sub right-inverse, NAT-sub left-inverse, NAT-cancel) compose to establish the involution; these are foundation properties the ASN already uses, requiring no design intent or implementation evidence.

## Issue 2: V-position subspace preservation cites the wrong ASN-0036 lemma
Reason: The fix is derivable from the ASN alone. OrdShiftHom (b) of ASN-0036 is already cited in this ASN (in the "OrdinalShift consumers" list and "Consequences of R-PRE"); replacing the misattributed S8-corollary citation with this lemma at both R-BLK sites is a pure citation correction needing no external input.
