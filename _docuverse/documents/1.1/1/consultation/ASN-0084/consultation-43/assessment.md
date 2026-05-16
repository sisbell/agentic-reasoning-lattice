# Channel Assignment — ASN-0084 review-43

**Date:** 2026-05-15 18:56

## Issue 1: R-WP label is structurally misleading
Reason: The fix is internal — rename the label or prove necessity. Both options are derivable from the ASN's own definitions (R-PRE conjuncts, postcondition equations); no design-intent or implementation evidence is required to choose the label or to construct counterexamples for R-PRE(i)/(ii).

## Issue 2: PermutationDisplacement Δ has decorative arithmetic in Phase 3
Reason: The fix is internal — option (a) restates Phase 3 in terms of π, which the ASN already defines and proves commutes with shift (R-COMM). Option (b) is a formal extension within the ASN's own algebraic vocabulary. Neither requires external context.

## Issue 3: No worked example at the boundary
Reason: The fix is internal — trace the minimum-size and empty-right-exterior cases using the operation definitions, R-PRE, R-PPERM/R-SPERM, and R-BLK already present in the ASN. The "Outside ⋃_k V(b_k)" branch of Phase 1 is fully specified within the ASN, so the trace is derivable.

## Issue 4: R-PRE(v) "non-independence" argument is incomplete
Reason: The fix is internal — the missing chain (ordinal-difference ≥ 1 → V-position cardinality ≥ 1 via R-PRE(iv) and D-SEQ from ASN-0036) is fully present in the ASN's own dependencies. The argument needs to be restated correctly, not re-derived from external sources.

## Issue 5: R-NS forward reference muddles dependency direction
Reason: The fix is internal — reframing the dependency to cite R-FRAME-P(a)/R-FRAME-S(a) and the piecewise definitions (not the full bijection well-definedness proofs) is a structural reorganization within the ASN. All referenced elements are defined here; no external context is needed.
