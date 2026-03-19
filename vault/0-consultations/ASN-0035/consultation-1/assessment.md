# Revision Categorization — ASN-0035 review-1

**Date:** 2026-03-14 15:27

## Issue 1: N2 quantifies over N, but the definition of N does not support the claim
Category: INTERNAL
Reason: The fix is either redefining N to include a root-prefix constraint or restricting N2's quantifier to Σ.nodes with an inductive derivation from N3 + BAPTIZE. All necessary definitions and properties are already in the ASN and ASN-0034.

## Issue 2: Initial state of Σ.nodes underspecified
Category: INTERNAL
Reason: Tightening "at least the root node" to exactly `{r}` follows from the ASN's own invariants (N3, N5). The correct initial state is derivable by requiring the stated invariants hold from genesis.

## Issue 3: N8 claims all invariants preserved but verifies only N3
Category: INTERNAL
Reason: The preservation arguments for N4, N5, and the structural properties (N9, N10, N16) are already present or derivable within the ASN. The fix is organizational — enumerate and cross-reference existing arguments rather than seek new evidence.

## Issue 4: No concrete example verifying BAPTIZE postconditions
Category: INTERNAL
Reason: The reviewer provides the exact trace to include. Applying BAPTIZE to concrete tumblers and checking postconditions is mechanical, requiring only the definitions already in the ASN.

## Issue 5: N0 asserts link validity without formal grounding
Category: INTERNAL
Reason: The reduction from link well-formedness to span well-formedness follows from existing vocabulary (endsets are sets of spans) and T12 (span well-formedness is arithmetic). This is a two-line derivation from material already in scope, or a scope trim deferring to the link ASN.
