# Channel Assignment — ASN-0084 review-38

**Date:** 2026-05-15 17:09

## Issue 1: Necessity sketch uses a counterexample that violates ASN-0036 invariants
Reason: The fix is internal — the reviewer provides a concrete well-formed counterexample (V_S(d) = {[1,1], ..., [1,5]} with C = ([1, 2], [1, 4], [1, 100])), and verifying it falsifies R-PRE(iv) while preserving D-CTG/D-SEQ uses only definitions and invariants already in the ASN.

## Issue 2: Non-S subspace handling is fragmented across the ASN
Reason: The fix is internal — every clause needed for a consolidated "Non-S subspace invariance" subsection is already present in R-PPERM/R-SPERM, R-FRAME-P/S, R-BLK's scope note, R-COMM, R-DISP, and R-WP; the work is structural reorganization, not new derivation.

## Issue 3: R-BLK Phase 1 "later cut falls in already-split run" argument leaves the no-skip case implicit
Reason: The fix is internal — tightening the prose to make the conditional ("if c_j ∈ V(b_k) originally") explicit, or to note that c_j outside V(b_k) is processed against a different run, relies only on Phase 1's own logic.

## Issue 4: "v_1 < v_1" phrasing in step (b) of the canonical decomposition
Reason: The fix is internal — a typographical correction matching TS4's direct substitution (`v₁ + k₂ > v₁` gives `v₁ > v₁`), with no semantic change.

## Issue 5: Width-bound dependence in R-PRE consequences not explicit at point of use
Reason: The fix is internal — a presentation choice between adding `w_μ ≥ 1` as an R-PRE clause or adding a forward-reference to the consequences subsection; both alternatives are derivable from existing CS2/CS3/CS4 and R-PRE(iv) content.
