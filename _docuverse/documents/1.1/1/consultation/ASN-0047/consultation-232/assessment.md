# Channel Assignment — ASN-0047 review-232

**Date:** 2026-06-01 10:15

## Issue 1: S8★ under K.μ⁻ — the named discharge fails to establish condition (c) for the content subspace
Reason: The fix is internal — it reapplies ASN-0036's S8 to the contracted content-subspace projection, whose preconditions (S2, S3★, S8a, S8-depth, S8-fin) the ASN already shows are restriction-preserved. No design intent or implementation evidence is needed.

## Issue 2: L1b subsequent-link derivation restates the same `inc(·,0)`-modifies-only-terminal fact twice
Reason: The fix is internal — it consolidates a duplicated derivation of a TA5(c)/TA5-SigValid structural fact already present in the ASN, with no semantic change. Neither channel is needed.
