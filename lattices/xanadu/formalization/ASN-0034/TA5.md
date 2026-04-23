## Increment for allocation

A separate operation, distinct from the shifting arithmetic, handles address allocation. When the system allocates a new address, it takes the highest existing address in a partition and produces the next one.

The *last significant position* `sig(t)` of a tumbler — defined in TA5-SIG — identifies the rightmost nonzero component, or `#t` when all components are zero. For valid addresses, `sig(t) = #t` (TA5-SigValid), so `inc(t, 0)` on a valid address increments the last component of the last field.

**TA5 (HierarchicalIncrement).** For tumbler `t ∈ T` and level `k ≥ 0`, there exists an operation `inc(t, k)` producing tumbler `t'` such that:

  (a) `t' > t` (strictly greater under T1),

  (b) when `k = 0`: `t'` agrees with `t` at every position other than `sig(t)`; when `k > 0`: `t'` agrees with `t` on all original positions,

  (c) when `k = 0` (*sibling*): `#t' = #t` and `t'_{sig(t)} = t_{sig(t)} + 1`,

  (d) when `k > 0` (*child*): `#t' = #t + k`, the `k - 1` intermediate positions `#t + 1, ..., #t + k - 1` are set to `0` (field separators), and the final position `#t + k` is set to `1` (the first child).

*Proof.* Let `t = t₁. ... .tₘ` where `m = #t`, and let `k ≥ 0`.

**Construction.** When `k = 0` (*sibling increment*): set `t'ᵢ = tᵢ` for all `i ≠ sig(t)`, and `t'_{sig(t)} = t_{sig(t)} + 1`. Then `#t' = m`.

When `k > 0` (*child creation*): set `t'ᵢ = tᵢ` for `1 ≤ i ≤ m`, set `t'ᵢ = 0` for `m + 1 ≤ i ≤ m + k - 1`, and set `t'_{m+k} = 1`. Then `#t' = m + k`.

In both cases `t'` is a finite sequence of natural numbers with length ≥ 1, so `t' ∈ T` by T0.

**Verification of (b).** For `k = 0`: by construction `t'ᵢ = tᵢ` for all `i ≠ sig(t)`. For `k > 0`: by construction `t'ᵢ = tᵢ` for all `1 ≤ i ≤ m`.

**Verification of (c).** When `k = 0`: `#t' = m = #t`, and `t'_{sig(t)} = t_{sig(t)} + 1` by construction.

**Verification of (d).** When `k > 0`: `#t' = m + k = #t + k`. Positions `m + 1` through `m + k - 1` are `0` (empty range when `k = 1`). Position `m + k` is `1`.

**Verification of (a).**

*Case `k = 0`.* Let `j = sig(t)`. By (b), `t'ᵢ = tᵢ` for all `i ≠ j`, so the tumblers agree on positions `1 ≤ i < j`. At position `j`, `t'_j = t_j + 1 > t_j` by NAT-addcompat's strict successor inequality. Since `j = sig(t) ≤ m = #t = #t'`, both tumblers have a component at `j`. T1 case (i) yields `t < t'`.

*Case `k > 0`.* By (b), the tumblers agree on positions `1 ≤ i ≤ m`. T1 case (ii) requires `#t + 1 ≤ #t'`. NAT-discrete (instantiated at `m = 0`, `n = k`) discharges its strict antecedent against the case hypothesis `0 < k` and yields `1 ≤ k`. NAT-addcompat's order-compatibility of addition (instantiated at `m = #t`, `p = 1`, `n = k`) lifts `1 ≤ k` to `#t + 1 ≤ #t + k = #t'`. T1 case (ii) yields `t < t'`. ∎

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `k ≥ 0`.
- *Definition:* `inc(t, k)`: when `k = 0`, modify position `sig(t)` (TA5-SIG) to `t_{sig(t)} + 1`; when `k > 0`, extend by `k` positions with `k - 1` zeros and final `1`.
- *Depends:*
  - T0 (CarrierSetDefinition) — characterisation of `T` as finite ℕ-sequences of length ≥ 1; discharges `t' ∈ T`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — addition closure instantiated at `(t_{sig(t)}, 1)` gives `t_{sig(t)} + 1 ∈ ℕ`, and at `(0, 1)` gives `0 + 1 ∈ ℕ`, with `1 ∈ ℕ` from the same axiom.
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — strict successor inequality `n < n + 1` for Case `k = 0`; left order-compatibility `1 ≤ k ⟹ #t + 1 ≤ #t + k` for Case `k > 0`.
  - NAT-zero (NatZeroMinimum) — `0 ∈ ℕ` supplies both the literal value of the `k − 1` field separators and the legal `m`-value for instantiating NAT-discrete at `m = 0`.
  - NAT-discrete (NatDiscreteness) — instantiated at `m = 0`, `n = k`; the strict antecedent `0 < k` is the case hypothesis itself, so the axiom delivers `1 ≤ k` directly.
  - T1 (LexicographicOrder) — case (i) at divergence position `sig(t)` for `k = 0`; case (ii) with proper-prefix `#t + 1 ≤ #t'` for `k > 0`.
  - TA5-SIG (LastSignificantPosition) — resolves `sig(t)` in the definition and postconditions (b), (c).
- *Postconditions:* `t' ∈ T`. (a) `t' > t` under T1. (b) When `k = 0`: `(A i : 1 ≤ i ≤ #t ∧ i ≠ sig(t) : t'ᵢ = tᵢ)`. When `k > 0`: `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)`. (c) When `k = 0`: `#t' = #t`, `t'_{sig(t)} = t_{sig(t)} + 1`. (d) When `k > 0`: `#t' = #t + k`, positions `#t + 1 ... #t + k - 1` are `0`, position `#t + k` is `1`.

`inc(t, 0)` does not produce the immediate successor of `t` in the total order. It produces the smallest same-length tumbler that agrees with `t` on positions `1, ..., sig(t) − 1` and has a strictly larger component at position `sig(t)`. When `sig(t) = #t` (which holds for valid addresses by TA5-SigValid), this is the next peer at the same hierarchical depth. When `sig(t) < #t`, same-length tumblers lie between `t` and `inc(t, 0)` — for example, `(2, 0, 1)` lies between `(2, 0, 0)` and `inc((2, 0, 0), 0) = (3, 0, 0)`. The gap between `t` and `inc(t, 0)` contains the entire subtree of `t`: all tumblers `t.x₁. ... .xₘ`. The true immediate successor in the total order is `t.0` by T1 case (ii).

For `k > 0`, `inc(t, k)` likewise does not produce the immediate successor: for `k = 1` the result is `t.1`; for `k = 2` the result is `t.0.1`. In both cases `t.0` lies strictly between `t` and the result. For address allocation this is harmless: allocation advances the counter past all existing addresses.

The conditions under which `inc` preserves T4 are established in TA5a: `inc(t, k)` preserves T4 iff `k ∈ {0, 1}`, or `k = 2` with `zeros(t) ≤ 2`; for `k ≥ 3`, `inc(t, k)` violates T4 by introducing adjacent zero separators.

| Label | Statement | Status |
|-------|-----------|--------|
| TA5 | `inc(t, k)` produces `t' > t` with same-length structure for `k = 0` (sibling) and extended structure for `k > 0` (child) | proved (this property) |
| TA5-SIG | `sig(t)` is the rightmost nonzero component position of `t`, or `#t` when all components are zero | definition (separate property) |
| TA5-SigValid | For every valid address satisfying T4, `sig(t) = #t` | proved (separate property) |
| TA5a | `inc(t, k)` preserves T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`; violated for `k ≥ 3` | proved (separate property) |
