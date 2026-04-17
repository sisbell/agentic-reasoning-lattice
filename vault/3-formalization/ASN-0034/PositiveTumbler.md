## Zero tumblers and positivity

Under T3, the tumblers `[0]`, `[0, 0]`, `[0, 0, 0]`, etc., are *distinct* elements of T — they have different lengths. Under T1, they form a chain: `[0] < [0, 0] < [0, 0, 0] < ...` by the prefix rule. There is no single "zero tumbler"; there are infinitely many all-zero tumblers.

**Definition (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff at least one of its components is nonzero: `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler is a *zero tumbler* iff every component is zero: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

The predicate `Pos(t)` is not written `t > 0`, because `>` already denotes T1's lexicographic ordering, and the two notions diverge. The all-zero tumbler `[0, 0]` exhibits the divergence concretely: under T1, `[0] < [0, 0]` by case (ii) — the prefix rule, since `[0]` is a proper prefix of `[0, 0]` — yet `¬Pos([0, 0])`, since every component of `[0, 0]` is zero. The converse direction does hold: `Pos(t)` implies `t` is T1-greater than every zero tumbler, as the following proof establishes.

Every positive tumbler is greater than every zero tumbler under T1.

*Proof.* Let `t ∈ T` with `Pos(t)` and let `z ∈ T` be a zero tumbler; we show `z < t`. Since `Pos(t)`, there exists a smallest index `k` with `1 ≤ k ≤ #t` and `tₖ ≠ 0`; for all `i < k` we have `tᵢ = 0`. Since `z` is a zero tumbler, `zᵢ = 0` for all `i ≤ #z`. We distinguish two cases by the relationship between `#z` and `k`.

*Case `#z ≥ k`.* For `1 ≤ i < k` we have `zᵢ = 0 = tᵢ`, establishing the T1 agreement condition. Since `k ≤ #z` and `k ≤ #t`, we have `k ≤ min(#z, #t)`, and `zₖ = 0 < tₖ` because `tₖ ≥ 1` as a nonzero natural number. By T1 case (i) with witness `k`, `z < t`.

*Case `#z < k`.* For `1 ≤ i ≤ #z` we have `i < k` (since `i ≤ #z < k`), whence `tᵢ = 0 = zᵢ`, establishing the T1 agreement condition at every position of `z`. From `#z < k ≤ #t` we obtain `#z + 1 ≤ #t`, so by T1 case (ii) with witness `#z + 1`, `z < t`. ∎

The condition `Pos(w)` in TA0 (WellDefinedAddition — forward reference, § Tumbler arithmetic below) excludes all all-zero displacements regardless of length.

*Formal Contract:*
- *Definition:* `Pos(t)` (positive) iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. Zero tumbler: `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Depends:* T0 (CarrierSetDefinition) — the carrier set `T`, the length `#t`, and the component projection `tᵢ` used in the Definition (`Pos(t)` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`) and in the zero-tumbler companion definition (`(A i : 1 ≤ i ≤ #t : tᵢ = 0)`) all come from T0's characterisation of T as finite sequences over ℕ with length ≥ 1; additionally, the postcondition proof's step `zₖ = 0 < tₖ` because `tₖ ≥ 1` as a nonzero natural number is licensed by T0's discreteness axiom (no `m ∈ ℕ` with `0 < m < 1`), so the "nonzero ⇒ `≥ 1`" inference is discharged from T0's ℕ properties rather than left implicit. T1 (LexicographicOrder) — the postcondition proof invokes T1 case (i) when `#z ≥ k` to conclude `z < t` from `zₖ = 0 < tₖ`, and T1 case (ii) when `#z < k` to conclude `z < t` from `z` being a proper prefix of `t`. TA0 (WellDefinedAddition) [forward reference — TA0 is stated in § Tumbler arithmetic, after this section] — the closing prose paragraph cites TA0's precondition `Pos(w)` to motivate the predicate's purpose within tumbler addition.
- *Postconditions:* `(A t ∈ T, z ∈ T : Pos(t) ∧ (A i : 1 ≤ i ≤ #z : zᵢ = 0) :: z < t)` — every positive tumbler is strictly greater under T1 than every zero tumbler of any length. This postcondition is the *canonical* statement of the zero-tumbler-below-positive-tumbler relation; TA6 (ZeroTumblers) conjunct 2 [forward reference — TA6 is stated in § Tumbler arithmetic, after this section] is the same fact with operand names swapped (TA6's `s` plays the role of `z` here), and Conjunct 2 cites this postcondition in place of an independent reproof. Any future tightening of this statement must be reflected at TA6 as well, so the pair can be checked for mutual consistency at one site each.
