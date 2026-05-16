# Channel Assignment — ASN-0084 review-40

**Date:** 2026-05-15 18:06

## Issue 1: CS3 necessity counterexample uses cuts that violate CS2
Reason: The fix is purely internal — correcting a lexicographic-ordering error against T1 (ASN-0034) and either substituting a valid cut sequence (e.g., ([1,2],[1,5],[2,1])) or restructuring to acknowledge CS3 as presupposed by R-PRE(iv)/(v). Neither design intent nor implementation evidence is needed; the fix is derivable from T1's definition and this ASN's own R-PRE machinery.
