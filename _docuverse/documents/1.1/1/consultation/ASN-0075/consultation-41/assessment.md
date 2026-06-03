# Channel Assignment — ASN-0075 review-41

**Date:** 2026-06-03 07:53

## Issue 1: D-RECONS leans on P4a without noting it is composite-boundary-scoped — and this, not P4★, is the substantive reason D-BOUND must be in the operation's contract
Reason: The review supplies the load-bearing external fact (ASN-0047's ExtendedReachableStateInvariants list P4a only at composite boundaries), and the ASN already models the identical composite-boundary treatment for P4★; the fix is to mirror that prose for P4a and tie D-BOUND to it. Internal.

## Issue 2: The `d_A = d_B` edge case mis-attributes an unconditional contradiction to D-EXH
Reason: The fix is a direct restatement using the range-membership contradiction the ASN already articulates verbatim for disjointness; no external evidence or intent is needed. Internal.

## Issue 3: Repeated composite-boundary / P4★ justifications accreted across sections (anti-bloat)
Reason: Pure editorial consolidation of three redundant in-document restatements into one at D-EXH; entirely derivable from the ASN's own structure. Internal.
