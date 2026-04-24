**T10a-N (AllocatorDisciplineNecessity).** T10a restricts the sibling stream of an allocator to `inc(·, 0)`. Relaxing this restriction to permit `inc(·, k)` with `k > 0` in the sibling stream falsifies T10a.2 (NonNestingSiblingPrefixes).

*Derivation.* Let `t₀ ∈ T`, fix `k > 0`, and let `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, k)` be co-sibling outputs of one allocator under the relaxation.

1. From TA5(d), conclude `#t₂ = #t₁ + k`.
2. From `k > 0` with NAT-zero (`0 ≤ k`) and NAT-discrete (at `m = 0`, no `n` satisfies `0 ≤ n < 1` except `n = 0`), conclude `k ≥ 1`.
3. From `1 ≤ k` by NAT-addcompat (order-compatibility, `m = #t₁, p = 1, n = k`), conclude `#t₁ + 1 ≤ #t₁ + k`.
4. From NAT-addcompat (strict successor at `n = #t₁`), conclude `#t₁ < #t₁ + 1`.
5. From (3), (4) by NAT-order (`m ≤ n ⟺ m < n ∨ m = n`), conclude `#t₁ < #t₁ + k = #t₂`.
6. From TA5(b) for `k > 0`, conclude `t₂` agrees with `t₁` at every position `1 ≤ i ≤ #t₁`.
7. From (5) by NAT-order, weaken to `#t₁ ≤ #t₂`.
8. From (6), (7) by Prefix, conclude `t₁ ≼ t₂`.

The strict inequality `#t₁ < #t₂` forces `t₁ ≠ t₂`, so `(t₁, t₂)` is a pair of distinct co-sibling outputs of one allocator with `t₁ ≼ t₂`, contradicting T10a.2. The construction is parametric in `k > 0`, so any relaxation admitting `inc(·, k)` with `k > 0` into the sibling stream witnesses such a pair. ∎

*Formal Contract:*
- *Preconditions:* T10a's sibling restriction is relaxed to permit `inc(·, k)` with any `k ≥ 0` in the sibling stream. `t₀ ∈ T`; `k > 0`; the allocator emits `t₁ = inc(t₀, 0)` and `t₂ = inc(t₁, k)` as co-sibling outputs.
- *Postconditions:* `t₁ ≼ t₂` with `t₁ ≠ t₂`, falsifying T10a.2 (NonNestingSiblingPrefixes). The `k = 0` sibling restriction is therefore necessary for T10a.2.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`.
  - NAT-zero (NatZeroMinimum) — supplies `0 ≤ k` to instantiate NAT-discrete at `m = 0`.
  - NAT-discrete (NatDiscreteness) — sharpens `k > 0` on ℕ to `k ≥ 1`.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — order-compatibility lifts `1 ≤ k` to `#t₁ + 1 ≤ #t₁ + k`; strict successor gives `#t₁ < #t₁ + 1`.
  - NAT-order (NatStrictTotalOrder) — chains the strict inequality and weakens `<` to `≤` for Prefix.
  - TA5 (HierarchicalIncrement) — (d) gives `#t₂ = #t₁ + k`; (b) gives agreement on positions `1..#t₁`.
  - Prefix (PrefixRelation) — converts agreement plus `#t₁ ≤ #t₂` into `t₁ ≼ t₂`.
  - T10a (AllocatorDiscipline) — the discipline whose relaxation is considered.
  - T10a.2 (NonNestingSiblingPrefixes) — the clause falsified by the constructed pair.
