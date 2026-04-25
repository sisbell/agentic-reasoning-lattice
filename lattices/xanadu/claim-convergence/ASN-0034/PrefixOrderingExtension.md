**PrefixOrderingExtension (PrefixOrderingExtension).** Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Proof.* Let `p₁ = p₁₁. ... .p₁ₘ` and `p₂ = p₂₁. ... .p₂ₙ`. By T1, `p₁ < p₂` gives a least position `k ≥ 1` with `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)` and one of two cases. Case (ii) would require `p₁ ≼ p₂`, contradicting non-nesting. So case (i) applies:

  (H1) `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)`.

  (H2) `k ≤ min(m, n)` and `p₁ₖ < p₂ₖ`.

Let `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`. By Prefix, `#a ≥ m` and `aᵢ = p₁ᵢ` for `1 ≤ i ≤ m`; `#b ≥ n` and `bᵢ = p₂ᵢ` for `1 ≤ i ≤ n`. Since `k ≤ m` and `k ≤ n`, we have `aₖ = p₁ₖ` and `bₖ = p₂ₖ`.

For `i` with `1 ≤ i < k`: `aᵢ = p₁ᵢ = p₂ᵢ = bᵢ` by Prefix, H1, and Prefix. At position `k`: `aₖ = p₁ₖ < p₂ₖ = bₖ` by H2. Since `k ≤ min(#a, #b)`, T1 case (i) yields `a < b`. ∎

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`; `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Depends:*
  - T1 (LexicographicOrder) — supplies divergence position `k` with `p₁ₖ < p₂ₖ`; re-applied to conclude `a < b`.
  - Prefix (PrefixRelation) — transfers component equality and length bounds from `p₁, p₂` onto `a, b`.
- *Postconditions:* `a < b` under T1.
