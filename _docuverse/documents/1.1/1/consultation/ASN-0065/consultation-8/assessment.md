# Revision Categorization — ASN-0065 review-8

**Date:** 2026-03-21 23:18

## Issue 1: CutSequence definition prevents rearranging the last document position
Category: INTERNAL
Reason: The fix is entirely derivable from the ASN's own content — the postcondition formulas already treat c_{n−1} as an exclusive upper bound that is never evaluated in M(d), and R-PRE(iv) already quantifies correctly. The issue is purely terminological ("V-positions" vs "tumblers") and the ASN itself identifies the exact resolution.
