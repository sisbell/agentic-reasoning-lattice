**T10a-N (AllocatorDisciplineNecessity).** Relaxing the `k = 0` restriction for siblings permits prefix nesting, violating the precondition of T10.

Suppose an allocator produces `t₁ = inc(t₀, 0)` followed by `t₂ = inc(t₁, 1)`. By TA5(c), `#t₁ = #t₀`. By TA5(d), `#t₂ = #t₁ + 1 = #t₀ + 1`, so `#t₁ < #t₂`. By TA5(b), `t₂` agrees with `t₁` on all components before the increment point. For `inc(t₁, 1)` with `k = 1`, the child construction (TA5(b)) copies all of `t₁` into positions `1, ..., #t₁` of `t₂`. So `t₂` agrees with `t₁` on positions `1, ..., #t₁`, and `#t₁ < #t₂`. These two facts — `#t₁ ≤ #t₂` and `∀i : 1 ≤ i ≤ #t₁ : t₂ᵢ = t₁ᵢ` — are precisely the conditions of the Prefix definition, so `t₁ ≼ t₂`.

The siblings nest. This violates the non-nesting precondition of T10 — any address extending `t₂` also extends `t₁`, so T10 cannot distinguish the two domains. The partition independence guarantee collapses. ∎

*Formal Contract:*
- *Preconditions:* `t₀ ∈ T`; allocator produces `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, 1)` (the `k = 0` sibling restriction is relaxed for the second step).
- *Postconditions:* `t₁ ≼ t₂` — prefix nesting occurs among the produced addresses, violating T10's non-nesting precondition (`p₁ ⋠ p₂ ∧ p₂ ⋠ p₁`).
