# Channel Assignment — ASN-0100 review-28

**Date:** 2026-06-03 09:56

## Issue 1: D-CTG★ proof glosses the depth ≥ 3 case
Reason: The fix invokes an existing foundation lemma (D-CTG-depth/SharedPrefixReduction, ASN-0036) or argues directly from the T1 tumbler order that off-prefix tuples fall outside [min, max] — both are pure ordering arguments derivable from the ASN's own cited machinery, needing neither design intent nor implementation evidence.

## Issue 2: S8★ existence/uniqueness applied to a restriction without the bridging lemma
Reason: The fix reroutes the existing M2/M12 citations through C1a (RestrictionDecomposition, ASN-0058), whose preconditions (functional restriction, finite domain, single common depth) are already discharged in the surrounding prose — a purely internal foundation-citation correction.
