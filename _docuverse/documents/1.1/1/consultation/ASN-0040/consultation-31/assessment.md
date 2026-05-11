# Channel Assignment — ASN-0040 review-31

**Date:** 2026-05-11 12:15

## Issue 1: B_type proof references B_fin before B_fin is established
Reason: Pure proof-ordering / structural issue internal to ASN-0040. The fix is a presentation decision (reorder, restructure, or joint induction) derivable from the proofs already present.

## Issue 2: Bop's correctness proof forward-references B1
Reason: Mutual recursion among Bop, B1, B10, and B_fin is an internal proof-structure issue. The fix (explicit joint induction or reordering with state-invariant appeals) is derivable from the ASN's own content.

## Issue 3: Misattribution in Bridge1 uniqueness proof
Reason: Pure citation correction. The correct source (definition of next / NextAddress) is already present in the ASN; no external input required.

## Issue 4: B_type's TA5(d) citation
Reason: Citation accuracy against ASN-0034's existing TA5 structure. Resolvable by inspecting TA5's stated postconditions; no design intent or implementation evidence needed.
