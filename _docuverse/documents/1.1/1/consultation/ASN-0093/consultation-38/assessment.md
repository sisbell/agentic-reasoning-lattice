# Channel Assignment — ASN-0093 review-38

**Date:** 2026-05-31 07:45

## Issue 1: ChainUniformLength is introduced but never used
Reason: Derivable from the ASN alone — the note already computes lengths directly in the worked example and no proof depends on ChainUniformLength, so the fix (cite it where load-bearing or delete the bullet and table row) is an internal editorial decision requiring no design intent or implementation evidence.

## Issue 2: Applicability enumeration lists results that are not load-bearing
Reason: Internal — determining which ASN-0040 results the note's own proofs actually consume (dropping B1/B9 and the permanence sentence) is settled by inspecting the note's existing argument structure, not by design intent or implementation evidence.

## Issue 3: L14 body derivation omits T7's preconditions
Reason: Internal — the Properties table and discharge matrix already state the correct premise set (StoreT4Validity for T4-validity, C1/L1 for zeros=3); the fix is making the body prose match what the note already establishes.

## Issue 4: Cross-document disjointness lemma states its corollary twice
Reason: Internal — removing the duplicated B7-vs-T10 statement from either the lemma statement or proof body is a pure deduplication derivable from the ASN's own text.
