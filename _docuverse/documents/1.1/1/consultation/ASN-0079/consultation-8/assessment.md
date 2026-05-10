# Revision Categorization — ASN-0079 review-8

**Date:** 2026-03-23 03:45

## Issue 1: F10 proof cites wrong foundation for functional-dependency claim
Category: INTERNAL
Reason: The fix is a citation correction — replacing L12 with a reference to the coverage definition in ASN-0043. The correct justification (coverage is a function of the span set, no other state component consulted) is already present in the ASN's reasoning and referenced definitions.

## Issue 2: F19 formalization does not match its prose
Category: INTERNAL
Reason: The mismatch between prose (non-matching population) and formula (total population) is a self-contained logical consistency issue. The review provides two concrete resolution options, both derivable from the existing text and Nelson's quoted constraint without needing external evidence.
