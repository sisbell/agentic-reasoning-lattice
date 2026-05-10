# Revision Categorization — ASN-0034 review-22

**Date:** 2026-03-26 03:18



## Issue 1: TA3-strict has spurious dependencies on T3 and TA6
Category: INTERNAL
Reason: The fix is purely about trimming the dependency graph based on which proof cases actually apply under the equal-length precondition — all reasoning is already present in the ASN.

## Issue 2: Dependency graph name mismatches
Category: INTERNAL
Reason: The canonical names are stated in the ASN body text; aligning the YAML fields is a mechanical consistency fix requiring no external evidence.

## Issue 3: TA7a verification overclaims S-membership for ⊖ when #w > #o
Category: INTERNAL
Reason: The fix requires qualifying S-membership claims with a length constraint or restricting the displacement definition — both derivable from the constructive definitions of TumblerSub and the S-membership criterion already in the ASN.
