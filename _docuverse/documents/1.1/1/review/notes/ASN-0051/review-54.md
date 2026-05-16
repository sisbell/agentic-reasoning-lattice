# Review of ASN-0051

## REVISE

### Issue 1: SV11 attainment scope conclusion is unjustified

**ASN-0051, "Multi-block (p ≥ 2) attainment — provably non-attained for m ≥ 2"**: "The witnessed attainment scope is precisely (m ≥ 1, p = 1); at every (m, p) with m ≥ 2 and p ≥ 2 the m · p bound is structurally loose."

**Problem**: The proof handles two sub-cases:
- *Disjoint-extent case* — correctly argues non-attainment via the suffix-overlap convexity argument.
- *Non-injective case (overlapping extents)* — only addresses the block-size barrier (sufficient when `min_k n_k < 2m − 1`).

But it does not address overlapping extents with sufficiently large blocks, where attainment IS possible. Counterexample at (m = 2, p = 2):
- Sequential siblings a₁ < a₂ < ... < a₁₀ in subspace s_C; V-positions v₁..v₁₅ in subspace s_C
- M(d): v₁..v₁₀ ↦ a₁..a₁₀ and v₁₁..v₁₅ ↦ a₆..a₁₀ (non-injective per S5)
- Block decomposition: β₁ = (v₁, a₁, 10), β₂ = (v₁₁, a₆, 5) — maximally merged because I-adjacency fails (a₆ ≠ a₁₁)
- Spans: s₁ = (a₁, a₈ ⊖ a₁), s₂ = (a₉, a₁₁ ⊖ a₉)
- All four (j, k) terms non-empty: {a₁..a₇}, {a₉, a₁₀}, {a₆, a₇}, {a₉, a₁₀}
- Within β₁: terms at offsets {0..6} and {8, 9} with gap at offset 7 — non-adjacent, non-overlapping
- Within β₂: terms at offsets {0, 1} and {3, 4} with gap at offset 2 — non-adjacent, non-overlapping
- Maximal fragment count = 4 = m · p. Attainment.

The closing sentence "the antecedent is jointly satisfiable by some concrete (B, e) only at p = 1" is therefore false.

The same issue affects (m = 1, p ≥ 2): a single span hitting multiple disjoint blocks attains m · p with no within-block coalescence possible — but the stated scope `(m ≥ 1, p = 1)` excludes this case.

**Required**: Either restrict the conclusion to cover only what the proof establishes (disjoint extents OR `min_k n_k < 2m − 1` overlapping), or supply a general argument for the non-injective large-block case. The SV11 biconditional itself is correct; only the attainment-scope conclusion needs revision. The Properties Introduced table's SV11 description (referencing the biconditional) is fine; the prose subsection is what overreaches.

META: The ASN remains in implementation-relevant specification territory — projection/discovery survivability is exactly the right level for state-and-transition invariants.

VERDICT: REVISE
