# Revision Categorization — ASN-0081 review-2

**Date:** 2026-04-09 18:55

## Issue 1: Local axioms VD, VP, VC duplicate foundation properties
Category: INTERNAL
Reason: The review identifies the exact ASN-0036 properties to cite (S8-depth, S8a, D-CTG). The fix is replacing local re-statements with citations — purely editorial.

## Issue 2: Contraction preconditions not formalized; positivity argument cites wrong property
Category: INTERNAL
Reason: The missing preconditions and the correct citation (S8a via `p ∈ V_S(d)` instead of VP) are all derivable from existing foundation properties already referenced by this ASN.

## Issue 3: Missing Istream frame condition
Category: INTERNAL
Reason: The prose already states content immutability; the fix is promoting it to a formal frame condition. The review provides the exact statement, anchored in S0.

## Issue 4: Post-state invariant preservation not derived
Category: INTERNAL
Reason: The review shows each derivation (S2, S3, D-CTG, D-MIN) follows in one or two steps from results already stated in this ASN and its cited foundations. No external evidence needed.

## Issue 5: Worked example omits boundary cases
Category: INTERNAL
Reason: Adding L=∅ and R=∅ cases is mechanical computation using the definitions and shift formula already present in the ASN.
