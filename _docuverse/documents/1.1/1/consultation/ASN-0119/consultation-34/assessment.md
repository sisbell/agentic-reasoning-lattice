# Channel Assignment — ASN-0119 review-34

**Date:** 2026-06-10 05:31

## Issue 1: RA3's derivation re-proves a fact RA2 already gives directly
Reason: Internal. The fix is a pure prose contraction — RA2 (`dom(M'(d)) = dom(M(d))`) and the already-stated "literally unchanged as a set" both live in the ASN; reading RA3 off them in one line needs no design intent or implementation evidence.

## Issue 2: The P4a paragraph restates conclusions it has just argued
Reason: Internal. The review explicitly preserves the load-bearing argument and asks only to delete an echo and a closing summary; this is a self-contained editorial deletion derivable from the ASN's own text.

## Issue 3: "suppress E and R … throughout" is contradicted by the discharge that follows
Reason: Internal. The corrected wording ("suppress from the state-tuple notation") is fixed by the ASN's own later by-name discharge of the `E`/`R` invariants; the facts (`E' = E`, `R' = R`, inertness) are already present, so no external channel is needed.
