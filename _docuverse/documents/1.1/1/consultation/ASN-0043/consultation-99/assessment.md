# Channel Assignment — ASN-0043 review-99

**Date:** 2026-05-30 13:30

## Issue 1: L11b invokes FSP without discharging FSP's `s_C`-residence hypothesis
Reason: The fix is purely structural — adding a precondition L11b already carries in its sibling lemma L9, and tightening FSP's L14a bullet to cite the scoped disjointness. All ingredients (FSP hypotheses, L0/L0a scoping, S3, L9's matching precondition) are present in the ASN.

## Issue 2: Synthesizing forward-pointer paragraph in *Home and Ownership* restates downstream claims without advancing them
Reason: Editorial deletion of a redundant restatement; the load-bearing clause (`home(a) = s = d`) and its cited support (L1c) are already in the ASN, and L2 stands on its own. No design intent or implementation evidence needed.
