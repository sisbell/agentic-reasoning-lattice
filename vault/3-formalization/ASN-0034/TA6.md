**TA6 (ZeroTumblers).** No zero tumbler is a valid address — no all-zero tumbler designates content. Every zero tumbler is less than every positive tumbler under T1.

  `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`

  `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`

*Proof (from T1, T4).* We prove each conjunct separately. Recall that T1 defines `a < b` on tumblers by: there exists a witness position `k ≥ 1` with `aᵢ = bᵢ` for all `i < k`, and either (i) `k ≤ min(#a, #b)` and `aₖ < bₖ`, or (ii) `k = #a + 1 ≤ #b` — that is, `a` is a proper prefix of `b`. Recall that T4 requires every valid address to satisfy `t₁ > 0` — the first component belongs to the node field, and the positive-component constraint requires every field component to be strictly positive.

**Conjunct 1** (invalidity): Let `t` be a zero tumbler, so `tᵢ = 0` for all `1 ≤ i ≤ #t`. Since `t ∈ T`, T0 guarantees `#t ≥ 1`, so `t₁` is defined and `t₁ = 0`. This violates T4's requirement `t₁ > 0`, so `t` is not a valid address.

**Conjunct 2** (ordering): Let `s` be a zero tumbler of length `m`, so `sᵢ = 0` for all `1 ≤ i ≤ m`. Let `t` be a tumbler of length `n` with at least one positive component — there exists `j` with `1 ≤ j ≤ n` and `tⱼ > 0`. We must show `s < t`.

Define `k = min({i : 1 ≤ i ≤ n : tᵢ > 0})` — the position of the first positive component in `t`. This minimum exists because `t` has at least one positive component. By minimality of `k`, we have `tᵢ = 0` for all `1 ≤ i < k`, and `tₖ > 0`.

*Case 1* (`k ≤ m`): For all positions `1 ≤ i < k`, `sᵢ = 0` (since `s` is a zero tumbler) and `tᵢ = 0` (by minimality of `k`), so `sᵢ = tᵢ`. At position `k`, `sₖ = 0 < tₖ` (since `tₖ > 0`). Since `k ≤ m` (case assumption) and `k ≤ n` (by definition of `k` as an element of `{1, …, n}`), we have `k ≤ min(m, n)` — this is a divergence within the shared length. T1 case (i) applies with witness `k`, giving `s < t`.

*Case 2* (`k > m`): For all positions `1 ≤ i ≤ m`, we have `i ≤ m < k`, so `tᵢ = 0` (by minimality of `k`) and `sᵢ = 0` (since `s` is a zero tumbler), giving `sᵢ = tᵢ`. The tumblers agree at every position of `s`. Since `m < k` and `k ≤ n`, we have `m < n`, so `m + 1 ≤ n`. T1 case (ii) applies with witness `m + 1`: `s` is a proper prefix of `t`, hence `s < t`. ∎

*Formal Contract:*
- *Depends:* T0 (CarrierSetDefinition) — Conjunct 1 uses T0's guarantee `#t ≥ 1` for all `t ∈ T` to establish that `t₁` is defined. T1 (LexicographicOrder) — Conjunct 2 invokes T1 case (i) at the first positive position of `t` and T1 case (ii) when `s` is a proper prefix of `t`. T4 (HierarchicalParsing) — Conjunct 1 relies on T4's requirement `t₁ > 0` to reject zero tumblers as valid addresses.
- *Postconditions:* (a) `(A t ∈ T : (A i : 1 ≤ i ≤ #t : tᵢ = 0) ⟹ t is not a valid address)`. (b) `(A s, t ∈ T : (A i : 1 ≤ i ≤ #s : sᵢ = 0) ∧ (E j : 1 ≤ j ≤ #t : tⱼ > 0) ⟹ s < t)`.

Zero tumblers serve as *sentinels*: they mark uninitialized values, denote "unbounded" when used as span endpoints, and act as lower bounds.
