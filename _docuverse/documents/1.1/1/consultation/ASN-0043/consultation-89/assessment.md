# Channel Assignment — ASN-0043 review-89

**Date:** 2026-05-30 11:04

## Issue 1: Notation paragraph enumerates a downstream consumer instead of advancing the definition
Reason: Pure deletion — the S7d sentence is removed and the same fact is already restated at the L9 selection step. No design-intent or implementation question is at stake; the fix is internal to the ASN.

## Issue 2: L3 prose develops at length a case the invariant already excludes
Reason: Compression of an already-present implementation walkthrough into one sentence. The conforming/non-conforming boundary is already stated by L3 and the closing sentence; trimming the `docreatelink` verb-by-verb account removes detail rather than asserting any new fact requiring verification.

## Issue 3: The invariant-vs-lemma distinction is explained defensively in two places
Reason: Both clauses are defended terminology, not proof content; the enumerated invariant lists in FSP and L11b already carry the distinction. Deletion is internal.

## Issue 4: L3 closing sentence restates the conjunct it just stated
Reason: The sentence paraphrases the formal conjunct `Σ.L(a).e₃ ≠ ∅` without adding constraint. Removing or folding it is derivable from the ASN's own text.
