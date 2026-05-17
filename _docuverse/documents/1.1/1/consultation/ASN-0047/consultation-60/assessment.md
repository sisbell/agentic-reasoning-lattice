# Channel Assignment — ASN-0047 review-60

**Date:** 2026-05-16 21:57

## Issue 1: K.δ combined `zeros` formula is incorrect for k = 0
Reason: Pure formal error. The correct case-split is already implicit in the per-sub-case statements and the ghost-base worked example (Step 2 confirms `zeros(e₂) = zeros(e₁) = 2` for k = 0). Fix is mechanical — derivable from the ASN's own content.

## Issue 2: K.μ⁻ admissibility precondition references a nonexistent "third subspace"
Reason: Pure formal slip — SC-NEQ fixes exactly two subspaces (s_C, s_L) throughout the ASN; the "third" phrasing is a writing artifact. Fix is rephrasing to match the two-subspace structure already established.

## Issue 3: Worked examples don't exercise NodeUniqueAllocation or NodeLineage non-vacuously
Reason: The abstract mechanism (case (i) precondition, NodeUniqueAllocation, NodeLineage, `n₀ ≼ e`) is fully specified in the ASN, and concrete forms like `[1, 2]` and the depth-1 multi-component shape are already cited in prose. The worked example just instantiates existing abstract content.

## Issue 4: SubAllocatorAxiom's "outside T10a's per-owner inc tree" framing conflicts with the structural producibility it later concedes
Reason: Presentation/ordering issue. Both halves of the reconciliation (operational spawning vs structural producibility, including the `b_C(d) = inc(d, 2)` chain) are already in the ASN; the fix is reordering and labeling the two framings explicitly. No external evidence needed.
