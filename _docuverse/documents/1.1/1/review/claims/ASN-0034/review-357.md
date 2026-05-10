# Regional Review — ASN-0034/T1 (cycle 3)

*2026-04-22 00:06*

Looking at the ASN, I'll check whether previously flagged issues are genuinely resolved and look for any new ones.

Resolved this cycle: `min(m,n)` is gone from Case 3; `≥` no longer appears in NAT-addcompat's contract (now stated with `≤`); NAT-cancel commentary cites "the NAT-* axioms of this ASN" rather than a T0 enumeration; NAT-discrete's Depends entry no longer claims a Case 3 role.

One new issue remains.

### `>` and `≥` on ℕ are used in T1's proof but never introduced

**Foundation**: NAT-order (NatStrictTotalOrder) — formal contract: "`(A n ∈ ℕ :: ¬(n < n))` … The non-strict relation `≤` on ℕ is defined by `m ≤ n ⟺ m < n ∨ m = n`." No definition of `>` or `≥` on ℕ appears here or in any other NAT-* axiom. T1's Abbreviations introduce `≥` only on T: "`a ≥ b` abbreviates `b ≤ a`."

**ASN**: T1 (LexicographicOrder), proof body uses both symbols on ℕ in several load-bearing steps:
- Transitivity, case `k₂ < k₁`: "NAT-addcompat gives `n + 1 > n`, so `k₂ > n ≥ k₁` by NAT-order transitivity, contradicting `k₂ < k₁`."
- Transitivity, case `k₁ < k₂`, T1(ii) sub-branch: "`k₁ = m + 1 ≤ n`, and `cₖ₁` exists, so `p ≥ m + 1`."
- Transitivity, sub-case (i, ii): "`k ≤ n` and `k = n + 1 ≤ p`, so `k > n`; contradiction."

**Issue**: The previous cycle's fix for the undefined-`≥` issue restated NAT-addcompat's contract in terms of `≤`, removing the contract-level dependence on `≥`. But T1's proof body still uses `>` and `≥` on ℕ at several genuinely load-bearing steps — including the central contradictions in two transitivity sub-cases. NAT-order supplies only `<` (axiomatic) and `≤` (defined); neither `>` nor `≥` is given for ℕ anywhere in this ASN. The tumbler-side `a ≥ b` is explicitly defined in T1's Abbreviations, making the absence of an analogous ℕ-side definition a visible asymmetry. A reader resolving "`k₂ > n ≥ k₁`" against the ASN's vocabulary has no stated definition to bind either symbol to.

**What needs resolving**: Either extend NAT-order's formal contract to introduce `>` and `≥` on ℕ (e.g., `m > n ⟺ n < m` and `m ≥ n ⟺ n ≤ m`), or rewrite T1's proof body to state these steps using only `<` and `≤` (for instance, "`n < n + 1`, so from `k₁ ≤ n` and `k₂ = n + 1` obtain `k₁ < k₂`"), so the proof remains within the vocabulary NAT-order actually establishes.

## Result

Regional review converged after 4 cycles.

*Elapsed: 2333s*
