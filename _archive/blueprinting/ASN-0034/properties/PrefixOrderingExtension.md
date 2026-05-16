**PrefixOrderingExtension (PrefixOrderingExtension).** Let `p₁, p₂ ∈ T` be tumblers such that `p₁ < p₂` and neither is a prefix of the other (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`). Then for every `a` extending `p₁` (`p₁ ≼ a`) and every `b` extending `p₂` (`p₂ ≼ b`), `a < b`.

*Proof.* We must show: `(A a, b ∈ T : p₁ ≼ a ∧ p₂ ≼ b : a < b)`, given that `p₁ < p₂` and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`.

Let `p₁ = p₁₁. ... .p₁ₘ` and `p₂ = p₂₁. ... .p₂ₙ`. The hypothesis `p₁ < p₂` means, by T1 (lexicographic order), that there exists a least position `k ≥ 1` such that `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)` and one of two cases holds. Case (ii) of T1 requires `p₁` to be a proper prefix of `p₂`, i.e., `k = m + 1 ≤ n`, which would give `p₁ ≼ p₂` — contradicting the hypothesis `p₁ ⋠ p₂`. Therefore case (i) of T1 applies: `k ≤ min(m, n)` and `p₁ₖ < p₂ₖ`. We record:

  (H1) `(A i : 1 ≤ i < k : p₁ᵢ = p₂ᵢ)` — the prefixes agree before position `k`.

  (H2) `k ≤ min(m, n)` and `p₁ₖ < p₂ₖ` — the prefixes diverge at position `k`.

Now let `a` and `b` be arbitrary tumblers with `p₁ ≼ a` and `p₂ ≼ b`. The prefix relation `p₁ ≼ a` means `#a ≥ m` and `aᵢ = p₁ᵢ` for all `1 ≤ i ≤ m`. Since `k ≤ m` (from H2, as `k ≤ min(m, n) ≤ m`), position `k` falls within the prefix, so `aₖ = p₁ₖ`. By the same reasoning, `p₂ ≼ b` gives `#b ≥ n` and `bᵢ = p₂ᵢ` for all `1 ≤ i ≤ n`; since `k ≤ n`, we have `bₖ = p₂ₖ`.

We now verify the two conditions required by T1 case (i) for `a < b`. First, agreement before position `k`: for each `i` with `1 ≤ i < k`, we have `aᵢ = p₁ᵢ` (from `p₁ ≼ a`, since `i < k ≤ m`) and `p₁ᵢ = p₂ᵢ` (from H1) and `p₂ᵢ = bᵢ` (from `p₂ ≼ b`, since `i < k ≤ n`), giving `aᵢ = bᵢ`. Second, strict inequality at position `k`: `aₖ = p₁ₖ < p₂ₖ = bₖ` (combining the prefix transfers with H2). Since `k ≤ min(#a, #b)` (as `k ≤ m ≤ #a` and `k ≤ n ≤ #b`), T1 case (i) applies, giving `a < b`.

Since `a` and `b` were arbitrary tumblers extending `p₁` and `p₂` respectively, the result holds universally: `(A a, b ∈ T : p₁ ≼ a ∧ p₂ ≼ b : a < b)`. ∎

*Formal Contract:*
- *Preconditions:* `p₁, p₂ ∈ T` with `p₁ < p₂` (T1) and `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` (non-nesting); `a, b ∈ T` with `p₁ ≼ a` and `p₂ ≼ b`.
- *Postconditions:* `a < b` under T1.
