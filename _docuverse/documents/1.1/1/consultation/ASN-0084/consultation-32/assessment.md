# Channel Assignment — ASN-0084 review-32

**Date:** 2026-05-15 13:44

## Issue 1: TS2 cited where TS5 is needed
Reason: Pure citation correction within the ASN's formal math; the ASN itself uses TS5 correctly elsewhere in the same proof, and the fix is mechanical replacement of one foundation-lemma label with another.

## Issue 2: R-WP and Q quantify over V_S(d) where they should quantify over dom(M(d))
Reason: Scope alignment derivable from the ASN alone — R-BLK's own statement and proof already operate over dom(M(d)) including non-S runs, so restating R-WP/Q to match is internal bookkeeping against ASN-0036's S8 and R-BLK as written.

## Issue 3: "Order-reversal" appeal is not derived from NAT-sub axioms
Reason: The required two-step derivation uses NAT-sub right-inverse and NAT-cancel (both already cited and used elsewhere in this same helper lemma), so the fix is internal to ASN-0034's named primitives.

## Issue 4: Premature "every invariant is maintained" claim
Reason: The fix restricts an expository sentence to what has actually been discharged at that point in the audit; the load-bearing lemma (R-BLK via R-WP) is already present later in the ASN, so the correction is a self-contained rewording.
