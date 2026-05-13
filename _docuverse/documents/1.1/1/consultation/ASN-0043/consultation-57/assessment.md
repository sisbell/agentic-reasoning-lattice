# Channel Assignment — ASN-0043 review-57

**Date:** 2026-05-13 12:15

## Issue 1: Chain-start premise for `home(a) = d` not formally captured
Reason: The fix is a purely formal tightening of L1c (or L1a) — adding the chain-start clause that the ASN's prose already presupposes and that downstream proofs (Home/Ownership, L11b) implicitly use. Nelson's design intent (home = creating document) and Gregory's evidence (`docreatelink` allocates under the creating document) are both already cited in the surrounding prose; the gap is in the formal invariant, not in design or evidence.
