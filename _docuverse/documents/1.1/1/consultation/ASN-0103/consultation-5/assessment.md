# Channel Assignment — ASN-0103 review-5

**Date:** 2026-06-05 00:32

## Issue 1: `max(D_A)` well-definedness is never established
Reason: Derivable from the ASN's own state model — `Σ₀.E = {n₀}` is finite and each `K.δ` transition (already the operation's decomposition) adds at most one entity, so `E` and hence `D_A ⊆ E` are finite. The reviewer supplies the exact one-line argument; it parallels ASN-0093's own `max` justification. No external channel needed.

## Issue 2: "next emission of `A_doc(A)`" overclaims relative to what is derived
Reason: Both offered fixes are internal. Contiguity of `E_doc ∩ S(A, 2)` follows by induction over `K.δ` from P1 (already cited) plus the operation's own frontier-picking discipline (`max(D_A)`), all within the ASN; alternatively the prose can simply be weakened to "a fresh address strictly exceeding `max(D_A)`," which the load-bearing claims (freshness, monotonicity, uniqueness) already support. Neither route requires design intent or implementation evidence.
