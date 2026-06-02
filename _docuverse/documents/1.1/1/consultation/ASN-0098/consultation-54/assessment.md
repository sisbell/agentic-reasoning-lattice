# Channel Assignment — ASN-0098 review-54

**Date:** 2026-06-02 16:23

## Issue 1: LP12b re-derives `dom(Σ.L) ⊆ F`, which LP-Sub already proves
Reason: Internal fix — LP-Sub is stated within the same ASN and proves exactly `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` from the same citations; replacing the duplicate derivation with a back-reference requires no design intent or implementation evidence.

## Issue 2: Achievability section is roadmap/meta-prose deferring to the worked example
Reason: Internal fix — deleting forward-pointing meta-prose and keeping the self-contained emission-frontier construction is a pure editorial operation on existing ASN content; the construction and its reliance on LP-Fin Corollary are already present.

## Issue 3: Rationale-for-`F`-definition prose accreted at two sites
Reason: Internal fix — both clauses justify the shape of the `F` definition rather than advancing a proof; the load-bearing membership facts are stated adjacently, so dropping the rationale needs no external input.

## Issue 4: Worked trace re-derives chain mechanics already established upstream
Reason: Internal fix — the chain length-uniformity, ordering, and injectivity facts are already fixed by cited ASN-0093 lemmas used identically in the F-definition and LP-Sub; collapsing to conclusion-plus-citation is derivable from the ASN alone.
