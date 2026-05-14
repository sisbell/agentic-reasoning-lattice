# Channel Assignment — ASN-0042 review-41

**Date:** 2026-05-14 05:44

## Issue 1: O12 cited where O13 is required (two instances)
Reason: Pure citation correction — both O12 and O13 are already defined in the ASN; the fix is swapping the cited label. Derivable from the ASN's own content.

## Issue 2: NestingByDelegation derivation list omits O15
Reason: Table update to match an already-existing proof body that explicitly invokes O15. Internal bookkeeping fix; no external evidence required.

## Issue 3: Delegation O1b preservation argument implicitly assumes O13 for existing-vs-existing case
Reason: Requires inserting an explicit O13 citation into an existing argument. The ASN already defines O13 and uses it elsewhere; the fix is derivable from internal content.

## Issue 4: O7(c) recursive-delegation construction proves existence but skips the verification chain
Reason: Requires spelling out an inductive verification of conditions (ii) and (vi) over the exhibited prefix family. The required reasoning uses only definitions and properties already established in the ASN (delegation conditions, prefix lengths, the NestingByDelegation case analysis).
