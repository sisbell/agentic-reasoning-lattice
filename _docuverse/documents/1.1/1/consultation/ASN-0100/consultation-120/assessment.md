# Channel Assignment — ASN-0100 review-120

**Date:** 2026-06-08 00:05

## Issue 1: "Split K.μ⁺" presented as decomposition freedom understates the contiguity constraint
Reason: Fully internal. The ASN already establishes D-CTG★/D-SEQ★ as per-state invariants holding at every intermediate (Atomicity section), so the constraint that a split must add Insertion-before-or-with Shifted-right to keep intermediates contiguous is derivable from the document's own invariant reasoning.

## Issue 2: Link-subspace out-of-scope stated redundantly (multiple-deferral pattern)
Reason: Fully internal. This is a purely editorial deletion of a redundant parenthetical; the scope boundary remains correctly stated in Bounding the Scope, requiring no design intent or implementation evidence.
