# Channel Assignment — ASN-0108 review-12

**Date:** 2026-06-05 05:17

## Issue 1: W9's buggy-reader failure mode is mischaracterized
Reason: The fix is internal — tracing the described reader's stop condition against an exact multiple `m = kN` is pure derivation from W9's own batch-size sequence, requiring no design intent or implementation evidence.

## Issue 2: W9a's closed-form count silently assumes fixed `N`
Reason: The fix is internal — W4 already isolates the "constant schedule `N_i = N`" restriction, so adding the matching qualifier to W9a is consistency repair against the ASN's own content.
