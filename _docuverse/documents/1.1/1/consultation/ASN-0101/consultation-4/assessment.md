# Channel Assignment — ASN-0101 review-4

**Date:** 2026-05-27 15:02

## Issue 1: D8 omits S4 from invariant preservation
Reason: Fix is mechanical — add S4 to Group (ii) with a one-line justification grounded in D2 (`dom(C') = dom(C)`) and S4's structural nature as a predicate over allocation events. Derivable from ASN-0047's classification and DEL's own frame.

## Issue 2: D8 Group (iii) mislabels per-state invariants as cross-transition
Reason: Fix is a labeling/organization correction grounded in ASN-0047's own classification of P6, P7, P8 as per-state (Class a) invariants. Either re-bucket or rename the group; no external evidence needed.

## Issue 3: Composite-substitute argument elides a precondition obstacle
Reason: K.μ~'s precondition `|dom_S(M(d))| ≥ 2` is already specified in ASN-0047; combining it with DEL's own preconditions yields the case-split (`n_S = 1` makes the composite unconstructible). The fix is internal to the foundation; atomicity argument can be tightened from the existing specs alone.
