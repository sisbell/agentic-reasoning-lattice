# Channel Assignment — ASN-0075 review-12

**Date:** 2026-05-25 16:27

## Issue 1: Edge-case condition is sufficient but mischaracterized as defining
Reason: The fix is internal. The formal predicates DELETED and CURRENT are already defined in the ASN, so weakening the condition to match the predicate (or labelling it as sufficient-only) is derivable from definitions already present.

## Issue 2: Q0 derivation invokes P4★ on a contradiction-target without naming the composite-boundary hypothesis
Reason: The fix is internal. D-EXH already characterizes P4★ as a composite-boundary property and D-OBS/D-RECONS establish SHOWDELETIONS as observational. Threading the reachability hypothesis through the Q0 wp computation uses only material already in the ASN.

## Issue 3: D-ACT case structure has an implicit "shorter length, same origin" sub-case
Reason: The fix is internal. The ASN already establishes that every emission of A_C(d) has element-field length exactly 2 (used in the "Longer length" case). The missing sub-case's vacuity follows from the same uniform-length fact already cited.

## Issue 4: D-IDENT's appeal to S3★ for transclusion integrity overstates the guarantee
Reason: The fix is internal. S3★ is invoked correctly elsewhere in this ASN (e.g., in the D-EXH proof's chain via S3★'s link clause and content clause), so restricting the D-IDENT citation to S3★'s content clause requires only re-scoping the existing reference.
