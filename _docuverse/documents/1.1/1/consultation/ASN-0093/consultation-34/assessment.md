# Channel Assignment — ASN-0093 review-34

**Date:** 2026-05-31 06:57

## Issue 1: C1b invariant body carries discharge rationale duplicated by the matrix
Reason: Purely editorial — moving an existing frame-preservation argument out of the invariant statement and deleting a back-pointer. No design intent or implementation evidence is at stake; the discharge content already lives in the matrix.

## Issue 2: L1c/C1c statements forward-reference the same downstream location the matrix already points to
Reason: Deleting redundant forward-reference sentences whose routing is already handled by the matrix. Internal to the document's own cross-reference structure.

## Issue 3: Scope "Provided" inventory duplicates the Properties Introduced table
Reason: Collapsing a duplicate enumeration into a one-line scope statement, deferring to the existing Properties Introduced table. No external input needed — both lists are already present in the ASN.

## Issue 4: Cross-document disjointness lemma derives chain disjointness twice
Reason: Removing a redundant derivation route; the T10 any-extension claim and B7 chain-disjointness citation are both already in the ASN, and the fix is choosing which to keep. The logical relationship between them is internal.

## Issue 5: simultaneous-induction framing re-enumerates the discharge tables' grouping
Reason: Trimming a bulleted re-listing that restates the tables' own grouping, keeping only the conjoined-IH sentence. Entirely internal editorial deduplication.
