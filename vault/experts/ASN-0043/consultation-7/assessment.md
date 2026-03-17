# Revision Categorization — ASN-0043 review-7

**Date:** 2026-03-17 00:28

## Issue 1: L11 formal statement is prose inside a quantifier
Category: INTERNAL
Reason: The fix is reformulating an existing property using precise predicates. All necessary ingredients (GlobalUniqueness, T9, the non-injectivity observation) are already present in the ASN and referenced dependencies — this is a notation/precision issue, not a knowledge gap.

## Issue 2: L10 and L13 prove overlapping results for identical span constructions; L10 is incomplete
Category: INTERNAL
Reason: The full proof already exists in L13's case analysis — L10 just needs to reference it. Factoring a shared lemma and completing the missing exclusion direction is pure reorganization of arguments already present in the ASN.

## Issue 3: Worked example L12 transition verification checks an address not in the pre-state
Category: INTERNAL
Reason: The error is in the logical structure of the worked example's state transition sequence. The fix — either naming intermediate states or removing the inapplicable check — requires only the definitions and transition semantics already stated in the ASN.
