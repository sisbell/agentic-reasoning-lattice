# Revision Categorization — ASN-0084 review-11

**Date:** 2026-04-10 11:41



## Issue 1: Properties table label collision on PermutationDisplacement
Category: INTERNAL
Reason: This is a naming/notation fix entirely within the ASN — choosing a distinct label for the LEMMA requires no external evidence, only editorial consistency.

## Issue 2: PermutationDisplacement uniformity — listed as LEMMA but not formally stated
Category: INTERNAL
Reason: The uniformity claim follows directly from the explicit R-PPERM/R-SPERM formulas already in the ASN. Formalizing it as a proper lemma with preconditions/postconditions requires only reorganizing and restating what is already present.

## Issue 3: Split and Merge B3 proofs are stated for M(d) specifically
Category: INTERNAL
Reason: The proofs use only B3 of the constituent blocks and TS3 (shift composition) — no M(d)-specific property is needed. Generalizing to an arbitrary arrangement requires only rewording the existing proofs to make the arrangement-independence explicit.
