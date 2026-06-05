# Channel Assignment — ASN-0113 review-13

**Date:** 2026-06-05 01:32

## Issue 1: W5 biconditional is false for an empty subspace
Reason: The fix is internal — the forward proof already assumes non-emptiness, and the empty case is handled in W0; adding `V_S(d) ≠ ∅` to W5's hypotheses and cross-referencing W0 is derivable from the ASN's own content.

## Issue 2: No weakest-precondition characterization of the result shape
Reason: The fix is internal — the ingredients (W-pre, W6, W7) already exist in the ASN; the wp statements for each result cardinality are a mechanical assembly of these claims, requiring no design intent or implementation evidence.
