**T4a (SyntacticEquivalence).** T4's field-segment constraint — stated positionally as (i) no two zeros are adjacent, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0` — is equivalent to the condition that every *field segment* of `t` is non-empty, where the field segments are the `zeros(t) + 1` maximal contiguous sub-sequences of non-zero positions delimited by the zeros.

Let `t ∈ T` be a tumbler with `zeros(t) ≤ 3`. Set `k = zeros(t) ∈ {0, 1, 2, 3}` with zeros at positions `s₁ < s₂ < … < s_k` (strict increase by NAT-order; the length `k` of this enumeration equals `zeros(t)` by NAT-card's enumeration characterisation of `|·|` applied at the zero-index subset `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0} ⊆ {1, …, #t}`, whose cardinality T4 identifies with `zeros(t)`). Set `s₀ = 0` and `s_{k+1} = #t + 1` as sentinels. The arithmetic in what follows — the numerals `2` and `3`, the sums `s_i + 1`, `s_i + 2`, and `#t + 1`, and the partial subtraction `#t − 1` — is grounded thus: NAT-closure posits `1 ∈ ℕ` and closes ℕ under addition, so `2 := 1 + 1 ∈ ℕ`, `3 := 2 + 1 ∈ ℕ`, and each of `s_i + 1`, `s_i + 2`, `#t + 1` lies in ℕ; NAT-sub's conditional-closure clause applied at the hypothesis `#t ≥ 1` (T0) and `1 ∈ ℕ` gives `#t − 1 ∈ ℕ`. The `k + 1` field segments of `t` are the index ranges `(s_i, s_{i+1})` for `i = 0, 1, …, k` — i.e. the component sub-sequences `t[s_i + 1 .. s_{i+1} - 1]`. A segment is non-empty precisely when `s_{i+1} ≥ s_i + 2`. Every index not in `{s₁, …, s_k}` is a non-zero position; by T0 the carrier is ℕ, NAT-zero gives `0 ≤ tᵢ`, and NAT-discrete at `m = 0` rules out `0 ≤ tᵢ < 1` under `tᵢ ≠ 0`, so such a position carries a strictly positive value.

*Forward.* Assume every field segment is non-empty. We derive each positional condition.

*Condition (ii): `t₁ ≠ 0`.* The first field segment is `t[1 .. s₁ - 1]` when `k ≥ 1`, or `t[1 .. #t]` when `k = 0`; in either case its first index is 1. Segment non-emptiness gives `s₁ ≥ 2` (when `k ≥ 1`) or `#t ≥ 1` (when `k = 0`), so index 1 lies in the segment and `t₁` is a non-zero component. Hence `t₁ ≠ 0`.

*Condition (iii): `t_{#t} ≠ 0`.* The last field segment is `t[s_k + 1 .. #t]` when `k ≥ 1`, or `t[1 .. #t]` when `k = 0`; in either case its last index is `#t`. Segment non-emptiness gives `s_k ≤ #t - 1` (when `k ≥ 1`) or `#t ≥ 1` (when `k = 0`), so index `#t` lies in the segment and `t_{#t}` is a non-zero component. Hence `t_{#t} ≠ 0`.

*Condition (i): no adjacent zeros.* Suppose for contradiction that `tᵢ = 0 ∧ tᵢ₊₁ = 0` for some `i` with `1 ≤ i < #t`. Then `i` and `i + 1` are consecutive zero positions — say `s_j = i` and `s_{j+1} = i + 1` — and the interior field segment `t[s_j + 1 .. s_{j+1} - 1] = t[i + 1 .. i]` has no indices, so it is empty. This contradicts segment non-emptiness. Hence no two zeros are adjacent.

*Reverse.* Assume conditions (i), (ii), and (iii) hold. We show every field segment is non-empty.

*First segment (`i = 0`).* The segment occupies indices 1 through `s₁ - 1` (or 1 through `#t` when `k = 0`). If `k = 0` the segment equals `t` itself, which has `#t ≥ 1` indices. If `k ≥ 1`, condition (ii) forces `t₁ ≠ 0`, so index 1 is not a zero position, and therefore `s₁ ≥ 2` — the segment has at least one index.

*Last segment (`i = k`).* The segment occupies indices `s_k + 1` through `#t` (when `k ≥ 1`). Condition (iii) forces `t_{#t} ≠ 0`, so index `#t` is not a zero position, and therefore `s_k ≤ #t - 1` — the segment has at least one index.

*Interior segments (`1 ≤ i < k`).* Each such segment occupies indices `s_i + 1` through `s_{i+1} - 1`. Condition (i) forbids `s_{i+1} = s_i + 1`, and since the zero positions are strictly increasing we already have `s_{i+1} ≥ s_i + 1`; together these give `s_{i+1} ≥ s_i + 2`, so the segment has at least one index.

All segments — first, interior, and last — are non-empty. ∎

*Formal Contract:*
- *Preconditions:* `t ∈ T` with `zeros(t) ≤ 3`. The field-segment constraint of full T4-validity is *not* assumed; it appears as the conclusion of the Forward direction and the local hypothesis of the Reverse direction.
- *Depends:*
  - T0 (CarrierSetDefinition) — fixes the carrier as ℕ; supplies `#t ≥ 1` as the precondition for `#t − 1 ∈ ℕ`.
  - NAT-zero (NatZeroMinimum) — supplies the lower bound `0 ≤ tᵢ`.
  - NAT-discrete (NatDiscreteness) — converts `0 ≤ tᵢ` and `tᵢ ≠ 0` into `tᵢ ≥ 1`.
  - NAT-order (NatStrictTotalOrder) — licenses the strictly increasing enumeration `s₁ < s₂ < … < s_k` and the position inequalities.
  - NAT-closure (NatArithmeticClosureAndIdentity) — supplies `1 ∈ ℕ` and closure of ℕ under addition, grounding the numerals `2 := 1 + 1 ∈ ℕ` and `3 := 2 + 1 ∈ ℕ` used in `s₁ ≥ 2` and `zeros(t) ≤ 3`, and the sums `s_i + 1`, `s_i + 2`, `#t + 1` used to name the sentinels and the interior-segment inequality.
  - NAT-sub (NatPartialSubtraction) — conditional-closure clause applied at `#t ≥ 1` (T0) and `1 ∈ ℕ` (NAT-closure) gives `#t − 1 ∈ ℕ`, making `s_k ≤ #t − 1` a comparison of two ℕ-elements.
  - NAT-card (NatFiniteSetCardinality) — via the enumeration characterisation of `|·|`, identifies the length `k` of the strictly increasing enumeration `s₁ < s₂ < … < s_k` of the zero-index subset `{i : 1 ≤ i ≤ #t ∧ tᵢ = 0} ⊆ {1, …, #t}` with `zeros(t)`, so that `k = zeros(t)`.
  - T4 (HierarchicalParsing) — supplies the positional conditions (i), (ii), (iii), the field-segment terminology, and the zero-count bound `zeros(t) ≤ 3`.
- *Postconditions:* The three positional conditions (i), (ii), (iii) hold if and only if every field segment of `t` is non-empty.
