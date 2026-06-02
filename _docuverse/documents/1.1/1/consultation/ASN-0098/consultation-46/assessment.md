# Channel Assignment — ASN-0098 review-46

**Date:** 2026-06-02 15:37

## Issue 1: LP12a summary table drops the enabledness conjunct the body insists on
Reason: Pure internal consistency fix — restore `enabled(K.μ⁻[d, R]) ∧ …` in the table to match the body's own total-correctness derivation. No design intent or implementation evidence required.

## Issue 2: LP20's "partition" of the projection range is asserted without the disjointness premise
Reason: The fix cites an existing foundational invariant (store-disjointness SD/L14) already named in the dependency frame; both alternatives (cite or downgrade to "exhaustive union") are derivable from the ASN and its foundations alone.

## Issue 3: Forward-referencing meta-prose explaining LP-Fin's significance before LP-Fin is stated
Reason: Deletion of a redundant pre-justification paragraph whose decidability point already lives at the tight definition's use-site. Purely internal editorial action.

## Issue 4: LP19 hypothesis carries a scope-disclaimer that imagines an excluded case and defers to LP9
Reason: Drop a disclaimer sentence narrating a case the per-V-position hypothesis already excludes. Internal scoping cleanup, no external input.

## Issue 5: LP-Fin restates the same divergence argument twice
Reason: Proof refactor — establish "`d` is a length-`#d` prefix of `d_0`" once and reuse it. Entirely derivable from the ASN's own proof structure.
