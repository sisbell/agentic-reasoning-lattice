# Channel Assignment — ASN-0084 review-24

**Date:** 2026-05-15 11:04

## Issue 1: D-SEQ cited for arbitrary depth-2 subspaces, but D-SEQ applies only to V_1(d)
Reason: The fix requires a design-intent decision (scope restriction to S=1 vs. generalization to all depth-2 subspaces) — that's Nelson. Gregory can clarify whether udanax-green's rearrangement operations are confined to the text subspace or apply across depth-2 subspaces.
Nelson question: Were cut-point rearrangements (pivot/swap) intended to apply only to the text subspace (S=1, where D-SEQ guarantees sequential V-positions without tombstones), or to all depth-2 subspaces including the link subspace (S=2) where sparse V_S(d) with tombstones is permitted?
Gregory question: In udanax-green, do region-transposition / arrangement-permutation operations operate only on the text subspace, or are they invoked on link or other depth-2 subspaces — and if the latter, how does the implementation handle sparse / tombstoned V-position ranges?

## Issue 2: Canonical decomposition step (c) handles forward extension only
Reason: The fix is derivable from the ASN's own content — the backward-extension branch is one line ("(c, b) mergeable contradicts the termination condition"), using only definitions and the termination invariant already established in step (c).

## Issue 3: Phase 1 "outside ⋃_k V(b_k)" case asserted but its uniqueness justification is informal
Reason: This is a mechanical rephrasing that follows from Issue 1's scope decision; once Issue 1 is settled, the rewording uses only R-PRE(iv) and the resolved scope, all internal to the ASN.

## Issue 4: Step (b)'s a₁ = a₂ derivation references TS5 and TS4 but with mixed-zero handling that should be tightened
Reason: The fix expands an existing case analysis using ASN-0034 properties (TS5, TS4, T1 irreflexivity) already cited or available in the ASN's dependency chain — purely internal proof tightening.
