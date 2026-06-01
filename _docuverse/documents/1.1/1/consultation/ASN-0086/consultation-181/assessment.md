# Channel Assignment — ASN-0086 review-181

**Date:** 2026-06-01 11:20

## Issue 1: Pre-computed sub-consequences parked far from their use sites (forward-reference accretion)
Reason: Pure relocation of existing prose to its consumption sites; the sub-consequences and their use sites are all present in the ASN, so the fix is derivable from the note's own content with no design-intent or implementation evidence needed.

## Issue 2: Forward reference from a result to the lemma it depends on
Reason: Pure reordering of lemmas already in the ASN; the review itself confirms L-ContiguousPrefix's dependencies (ASN-0093 lemmas, clauses (b)/(c)) and that it does not depend on R0, so the fix is internal.

## Issue 3: Defensive "why the operation is partial" prose in a definition slot
Reason: Editorial restatement of the domain as a fact, drawing only on the substrate-conforming sub-domain already defined in the ASN; no external channel needed.
