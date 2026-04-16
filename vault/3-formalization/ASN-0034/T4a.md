**T4a (SyntacticEquivalence).** T4's field-segment constraint — stated positionally as (i) no two zeros are adjacent, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0` — is equivalent, under T4's positive-component constraint, to the condition that every *field segment* of `t` is non-empty, where the field segments are the `zeros(t) + 1` maximal contiguous sub-sequences of non-zero positions delimited by the zeros. T4 asserts the positional form of this constraint directly; this theorem records the equivalent reading in terms of segment non-emptiness. Once T4c (LevelDetermination) assigns the hierarchical labels Node, User, Document, Element to the segments in order, T4a reads as the semantic statement that every field present in an address has at least one component — but the equivalence itself is proven here without appeal to those labels.

Let `t` be an address tumbler with zeros at positions `p₁ < p₂ < … < pₖ`, where `k = zeros(t) ∈ {0, 1, 2, 3}`. Set `p₀ = 0` and `p_{k+1} = #t + 1` as sentinels. The `k + 1` field segments of `t` are then the index ranges `(p_i, p_{i+1})` for `i = 0, 1, …, k` — i.e. the component sub-sequences `t[p_i + 1 .. p_{i+1} - 1]`. A segment is non-empty precisely when `p_{i+1} ≥ p_i + 2`. The positive-component constraint requires every non-zero component of `t` to be strictly positive, so every index that is *not* in `{p₁, …, pₖ}` is a positive component.

*Forward.* Assume every field segment is non-empty, and that the positive-component constraint holds. We derive each positional condition.

*Condition (ii): `t₁ ≠ 0`.* The first field segment is `t[1 .. p₁ - 1]` when `k ≥ 1`, or `t[1 .. #t]` when `k = 0`; in either case its first index is 1. Segment non-emptiness gives `p₁ ≥ 2` (when `k ≥ 1`) or `#t ≥ 1` (when `k = 0`), so index 1 lies in the segment and `t₁` is a non-zero component. Hence `t₁ ≠ 0`.

*Condition (iii): `t_{#t} ≠ 0`.* The last field segment is `t[p_k + 1 .. #t]` when `k ≥ 1`, or `t[1 .. #t]` when `k = 0`; in either case its last index is `#t`. Segment non-emptiness gives `p_k ≤ #t - 1` (when `k ≥ 1`) or `#t ≥ 1` (when `k = 0`), so index `#t` lies in the segment and `t_{#t}` is a non-zero component. Hence `t_{#t} ≠ 0`.

*Condition (i): no adjacent zeros.* Suppose for contradiction that `tᵢ = 0 ∧ tᵢ₊₁ = 0` for some `i` with `1 ≤ i < #t`. Then `i` and `i + 1` are consecutive zero positions — say `p_j = i` and `p_{j+1} = i + 1` — and the interior field segment `t[p_j + 1 .. p_{j+1} - 1] = t[i + 1 .. i]` has no indices, so it is empty. This contradicts segment non-emptiness. Hence no two zeros are adjacent.

*Reverse.* Assume conditions (i), (ii), and (iii) hold. We show every field segment is non-empty.

*First segment (`i = 0`).* The segment occupies indices 1 through `p₁ - 1` (or 1 through `#t` when `k = 0`). If `k = 0` the segment equals `t` itself, which has `#t ≥ 1` indices. If `k ≥ 1`, condition (ii) forces `t₁ ≠ 0`, so index 1 is not a zero position, and therefore `p₁ ≥ 2` — the segment has at least one index.

*Last segment (`i = k`).* The segment occupies indices `p_k + 1` through `#t` (when `k ≥ 1`). Condition (iii) forces `t_{#t} ≠ 0`, so index `#t` is not a zero position, and therefore `p_k ≤ #t - 1` — the segment has at least one index.

*Interior segments (`1 ≤ i < k`).* Each such segment occupies indices `p_i + 1` through `p_{i+1} - 1`. Condition (i) forbids `p_{i+1} = p_i + 1`, and since the zero positions are strictly increasing we already have `p_{i+1} ≥ p_i + 1`; together these give `p_{i+1} ≥ p_i + 2`, so the segment has at least one index.

All segments — first, interior, and last — are non-empty. ∎

*Formal Contract:*
- *Preconditions:* `t` is an address tumbler satisfying T4's positive-component constraint (`tᵢ > 0` for every non-zero component).
- *Postconditions:* The three positional conditions of T4's field-segment constraint — (i) no two zeros are adjacent, (ii) `t₁ ≠ 0`, (iii) `t_{#t} ≠ 0` — hold if and only if every field segment of `t` (a maximal contiguous sub-sequence of non-zero positions delimited by the zeros of `t`) is non-empty. Once T4c assigns hierarchical labels to segments, this is equivalent to the semantic statement that every present field has at least one component.
