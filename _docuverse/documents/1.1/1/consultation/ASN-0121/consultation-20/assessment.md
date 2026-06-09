# Channel Assignment — ASN-0121 review-20

**Date:** 2026-06-09 02:28

## Issue 1: FL-WP omits the fresh-retraction-link entry, a third result-changing case
Reason: The fix is internal. FL-DEF already forces any addressable link satisfying `sat` into the result with no design freedom, and the wp for a fresh retraction link is a mechanical combination of FL-WP(a)'s fresh-entry template with FL-WP(b)'s singleton `L_R` extension `L_R^{Σ'} = L_R^Σ ∪ {(b, ∅, G')}` and the self-retraction conjunct FL-WP(b) already names — all machinery present in the ASN, so no design-intent or implementation evidence is required to compute the third case.
