# Channel Assignment — ASN-0101 review-3

**Date:** 2026-05-27 14:45

## Issue 1: D8 Group (i) misrepresents the link-subspace re-mapping case
Reason: The fix is internal — the corrected argument uses pre-state CL-OWN and CL-UNIQ on V_{s_L}(d) and the disjointness of L and R, all of which are already defined within the ASN's D0 effect specification.

## Issue 2: Worked example verifies D9 only hypothetically
Reason: The fix is internal — extending the worked example requires only the endset/coverage/project semantics already cited from ASN-0053 and the shift function already computed in the example. No new design intent or implementation evidence is needed to construct a concrete link and verify D9's third-bullet equation.

## Issue 3: D9 first-bullet justification omits D3 citation
Reason: The fix is internal — D3 is an in-ASN claim and the omission is a straightforward citation completion to match the parallel third-bullet argument.
