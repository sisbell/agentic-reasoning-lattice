# Channel Assignment — ASN-0040 review-25

**Date:** 2026-05-11 10:35

## Issue 1: B1 proof — sub-case (B) listing is incomplete and contradicts sub-case (C)
Reason: The fix is purely textual — extend an enumeration in B1's sub-case (B) to include the trailing-zero + d=2 configuration. The propagation mechanism (TA5(d)'s separator adjoining p's trailing zero) is already articulated within this ASN's own B6 sub-case (b). No external channels needed.

## Issue 2: Mutual forward references between B1 and B6 proofs
Reason: This is a presentation/organization issue within the ASN. All three resolution options (promote stream-identity to a labeled property, inline the case-propagation argument, or reorder B6 before B1) are restructurings of arguments already present in the text. No external channels needed.

## Issue 3: TA5a restated two different ways within the same ASN
Reason: The canonical TA5a statement lives in ASN-0034 (a sibling spec doc in this project), and the reviewer has already identified which restatement form matches it. The fix is to align both citations to the canonical form. No external channels needed.
