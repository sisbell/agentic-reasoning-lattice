# Channel Assignment — ASN-0102 review-30

**Date:** 2026-06-07 21:48

## Issue 1: S8-fin discharge rests on an incorrect justification
Reason: Internal fix. The corrected discharge follows from S8-fin at Σ (pre-state domain finite) plus the fact that COPY adds exactly `W = (+ j : 1 ≤ j ≤ k : n_j)` positions, a finite sum already defined in the ASN — no design intent or implementation evidence required.

## Issue 2: S8-depth discharge mis-stated for the empty-subspace first insertion
Reason: Internal fix. X16 already establishes the depth correctly for both the inherited (`n_S ≥ 1`) and chosen-and-pinned (`n_S = 0`) cases within the ASN; the repair merely re-routes the X14 citation through X16.

## Issue 3: Scope-rationale and identity-justification prose (anti-bloat)
Reason: Internal fix. Pure deletion/compression — the standalone-composite restriction already excludes the scoped case, and P2's identity rests on a bare ASN-0047 citation; no external channel bears on removing explanatory accretion.
