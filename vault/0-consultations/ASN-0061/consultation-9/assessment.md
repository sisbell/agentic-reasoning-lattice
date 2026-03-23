# Revision Categorization — ASN-0061 review-9

**Date:** 2026-03-22 23:13



## Issue 1: K.μ⁺ preconditions D-CTG and D-MIN not verified in composite transition
Category: INTERNAL
Reason: The review itself supplies the complete argument for both D-CTG and D-MIN verification at each step. All required properties (D-SEP, D-BJ, D-MIN on the pre-state) are already established within the ASN.

## Issue 2: D-MIN preservation absent from D-DP, invariant verification, and Properties Introduced
Category: INTERNAL
Reason: D-MIN is already defined in cited ASNs (ASN-0036, ASN-0047) and its preservation argument follows the same pattern as D-CTG using facts already present in this ASN. The fix is editorial — expanding D-DP's scope and updating the table — requiring no external evidence.
