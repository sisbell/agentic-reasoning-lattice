# Channel Assignment — ASN-0099 review-58

**Date:** 2026-06-03 09:49

## Issue 1: Silent-projection uniqueness characterization is false as stated
Reason: The fix is a self-contained logical correction — strengthen condition (i)'s upper bound from `ran(Σ.M(d))` to the image of `R`, making (i)+(ii) mutual inclusions, and dispatch the constant-`ran` counterexample. The corrected bound and the witnessing-V-position-in-`R` argument are derivable entirely from the ASN's own definitions of `image` and silent projection; no design intent or implementation evidence is required.
