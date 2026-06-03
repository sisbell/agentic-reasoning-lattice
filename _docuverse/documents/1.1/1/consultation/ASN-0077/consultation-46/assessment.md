# Channel Assignment — ASN-0077 review-46

**Date:** 2026-06-03 08:56

## Issue 1: `origins_V` finiteness asserted for the I-span lift but never for the V-span lift
Reason: The fix is derivable from the ASN's own content — it parallels the existing `origins_I` finiteness note using S8-fin (ASN-0036), which the ASN already cites (e.g., in C1a's preconditions). No design intent or implementation evidence is needed; the image of a finite set under a total function is finite.
