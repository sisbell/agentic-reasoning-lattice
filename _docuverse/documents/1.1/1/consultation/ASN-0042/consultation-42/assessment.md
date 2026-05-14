# Channel Assignment — ASN-0042 review-42

**Date:** 2026-05-14 06:03

## Issue 1: O10's Form B analysis has imprecise quantifier scope
Reason: The fix is a quantifier-scoping correction internal to the proof — restrict the PrefixBaptismCoupling argument to length-(#pfx(π)+2) Form B sub-delegates and scope or drop S'. Fully derivable from existing machinery (PrefixBaptismCoupling, B1, the length argument already in the proof).

## Issue 2: Worked example omits the field-opening boundary case of O10
Reason: Adding the `hwm_0 = 0` scenario uses only the ASN's own definitions (next, hwm, TA5(d), O10's proof structure) and the existing worked-example principals. No design-intent or implementation evidence is required to exhibit the missing case.

## Issue 3: O7(c)'s recursive-chain construction is informal
Reason: The strengthening cites NestingByDelegation (already established in the ASN) to constrain non-chain principals to the non-nesting disjunct relative to pfx(π_{k+1}). The fix is derivable from the ASN's own content.
