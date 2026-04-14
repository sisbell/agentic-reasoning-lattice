## Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one. This is not addition of a width; it is advancement of a counter at a specified hierarchical level.

The *last significant position* `sig(t)` of a tumbler — defined in TA5-SIG — identifies the rightmost nonzero component, or `#t` when all components are zero. For valid addresses, `sig(t) = #t` (TA5-SigValid), so `inc(t, 0)` on a valid address increments the last component of the last field, modifying only within that field and preserving the hierarchical structure.

**TA5 (HierarchicalIncrement).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) `t'` agrees with `t` on all components before the increment point,

  (c) when `k = 0` (*sibling*): `#t' = #t`, and `t'` differs from `t` only at position `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

*Proof.* We must show that for every `t ∈ T` and `k ≥ 0`, the construction below produces a tumbler `t' = inc(t, k)` satisfying all four postconditions. Recall that `sig(t)` denotes the last significant position of `t`: when `t` has at least one nonzero component, `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`; when every component of `t` is zero, `sig(t) = #t`.

**Construction.** Let `t = t₁. ... .tₘ` where `m = #t`, and let `k ≥ 0`. Define `t' = inc(t, k)` by cases.

When `k = 0` (*sibling increment*): set `t'ᵢ = tᵢ` for all `i ≠ sig(t)`, and `t'_{sig(t)} = t_{sig(t)} + 1`. The result has the same length: `#t' = m`.

When `k > 0` (*child creation*): set `t'ᵢ = tᵢ` for `1 ≤ i ≤ m`, set `t'ᵢ = 0` for `m + 1 ≤ i ≤ m + k - 1` (the `k - 1` field separators), and set `t'_{m+k} = 1` (the first child). The result has length `#t' = m + k`.

In both cases `t'` is a finite sequence of natural numbers with length ≥ 1, so `t' ∈ T`.

**Verification of (b)** (agreement before the increment point). For `k = 0`: by construction `t'ᵢ = tᵢ` for all `i` with `1 ≤ i < sig(t)`, since only position `sig(t)` is modified. For `k > 0`: by construction `t'ᵢ = tᵢ` for all `1 ≤ i ≤ m`, so `t'` agrees with `t` on every original position.

**Verification of (c)** (sibling structure). When `k = 0`: `#t' = m = #t` by construction. The only modified position is `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. Every other position retains its original value.

**Verification of (d)** (child structure). When `k > 0`: `#t' = m + k = #t + k` by construction. Positions `m + 1` through `m + k - 1` are `0` (field separators) — when `k = 1` this range is empty, so no separators are introduced. Position `m + k` is `1` (the first child).

**Verification of (a)** (`t' > t`). We establish `t < t'` under the lexicographic order T1, treating each case separately.

*Case `k = 0`.* Let `j = sig(t)`. By construction, `t'ᵢ = tᵢ` for all `i ≠ j`, so in particular the tumblers agree at every position `1 ≤ i < j` — this is part (b). At position `j`: `t'_j = t_j + 1 > t_j`, since `n + 1 > n` for every `n ∈ ℕ`. Since `j = sig(t) ≤ m` and `#t' = m`, we have `j ≤ min(#t, #t') = m`, so both tumblers have a component at position `j`. By T1 case (i) with divergence position `j`, the agreement on positions `1, ..., j - 1` and the strict inequality `t_j < t'_j` yield `t < t'`.

*Case `k > 0`.* By part (b), `t'ᵢ = tᵢ` for all `1 ≤ i ≤ m` — the tumblers agree on every position of `t`. Since `#t' = m + k > m = #t`, the tumblers agree at every position up to `#t`, and `t'` has further components beyond position `m`. T1 case (ii) applies with witness `m + 1 = #t + 1 ≤ #t' = m + k`: `t` is a proper prefix of `t'`, giving `t < t'`. ∎

*Formal Contract:*
- *Definition:* `inc(t, k)` for `t ∈ T`, `k ≥ 0`: when `k = 0`, modify position `sig(t)` to `t_{sig(t)} + 1`; when `k > 0`, extend by `k` positions with `k - 1` zeros and final `1`.
- *Postconditions:* (a) `t' > t` under T1. (b) When `k = 0`: `(A i : 1 ≤ i < sig(t) : t'ᵢ = tᵢ)`. When `k > 0`: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)`. (c) When `k = 0`: `#t' = #t`, modification only at `sig(t)`, where `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, positions `#t + 1 ... #t + k - 1` are `0`, position `#t + k` is `1`.

Gregory's analysis reveals a critical distinction: `inc(t, 0)` does NOT produce the immediate successor of `t` in the total order. It produces the *next peer* at the same hierarchical depth — the smallest tumbler with the same length that is strictly greater than `t`. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers of the form `t.x₁. ... .xₘ` for any `m ≥ 1` and any `x₁ ≥ 0`. The true immediate successor in the total order is `t.0` — the zero-extension — by the prefix convention (T1 case (ii)). For any `k > 0`, `inc(t, k)` does NOT produce the immediate successor of `t` in the total order. For `k = 1` the result is `t.1`; for `k = 2` the result is `t.0.1`. In both cases, `t.0` (the true immediate successor) lies strictly between `t` and the result. The gap between `t` and `inc(t, k)` contains `t`'s entire subtree of zero-extensions. For address allocation, the distinction is harmless: allocation cares about advancing the counter past all existing addresses, not about visiting every point in the total order.

The conditions under which `inc` preserves the structural validity constraint T4 — including the boundary on `k` and the role of `zeros(t)` — are established in TA5a (IncrementPreservesT4).

| Label | Statement | Status |
|-------|-----------|--------|
| TA5 | `inc(t, k)` produces `t' > t` with same-length structure for `k = 0` (sibling) and extended structure for `k > 0` (child) | introduced |
| TA5-SIG | `sig(t)` is the rightmost nonzero component position of `t`, or `#t` when all components are zero | introduced |
| TA5-SigValid | For every valid address satisfying T4, `sig(t) = #t` | proved |
| TA5a | `inc(t, k)` preserves T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`; violated for `k ≥ 3` | proved |
