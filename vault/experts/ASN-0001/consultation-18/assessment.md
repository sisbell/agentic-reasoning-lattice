# Revision Categorization — ASN-0001 review-18

**Date:** 2026-03-06 11:00

## Issue 1: TA3 strict order preservation is too strong
Category: INTERNAL
Reason: The fix is fully derivable from the ASN's own definitions and the Dafny counterexample provided. The constructive definition of subtraction with zero-padding, the proof structure, and the proposed weak/strict split all follow from content already present in the ASN — no external design intent or implementation evidence is needed.
