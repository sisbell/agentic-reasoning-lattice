# Channel Assignment — ASN-0121 review-4

**Date:** 2026-06-09 01:25

## Issue 1: nullified-monotonicity argument leaves K.δ uncovered
Reason: Internal fix. The companion link-store argument in the same paragraph already establishes the needed catch-all ("only K.λ touches the link store... every other operation framing `Σ.L` fixed"), which covers K.δ; the fix restructures the `nullified` argument to ride on that same fact (nullified is a function of `Σ.L` via `L_R^Σ`, K.δ frames `Σ.L` fixed). No design intent or implementation evidence required.
