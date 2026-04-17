**TA-strict (StrictIncrease).** `(A a ∈ T, Pos(w) : a ⊕ w > a)` (where `a ⊕ w` is well-defined, i.e., `k ≤ #a` per TA0).

Without TA-strict, the axioms admit a degenerate model in which `a ⊕ w = a` for all `a, w`. This no-op model satisfies TA0 (result is in T), TA1 (if `a < b` then `a < b` — the consequent is unchanged), and TA4 (`(a ⊕ w) ⊖ w = a ⊖ w = a` if subtraction is equally degenerate). Every axiom is satisfied, yet spans are empty — the interval `[s, s ⊕ ℓ)` collapses to `[s, s)`. TA-strict excludes this model and ensures that advancing by a positive displacement moves forward. T12 (span well-definedness) depends on this directly.

*Proof.* We show that for all `a ∈ T` and `Pos(w)` with action point `k ≤ #a`, the advanced position `a ⊕ w` is strictly greater than `a` under T1.

Let `a = [a₁, ..., aₘ]` and `w = [w₁, ..., wₙ]` with `Pos(w)`. The action point `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` exists because `Pos(w)`, and the TA0 precondition gives `k ≤ m`. Let `r = a ⊕ w`. By TA0, `r ∈ T` with `#r = n`, so the T1 comparison between `r` and `a` is well-defined.

We establish a witness for `r > a` under T1's definition. The TumblerAdd construction defines `r` in three regions: `rᵢ = aᵢ` for `1 ≤ i < k`, `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `k < i ≤ n`.

*Agreement before position `k`.* For every `i` with `1 ≤ i < k`, `rᵢ = aᵢ` — the prefix-copy rule of TumblerAdd reproduces the start position exactly. So `rᵢ = aᵢ` for all `i < k`.

*Strict increase at position `k`.* By definition of action point, `wₖ > 0`. Therefore `rₖ = aₖ + wₖ > aₖ`, since adding a positive natural number to a non-negative one yields a strictly larger result. Position `k` satisfies `k ≤ m = #a` (the TA0 precondition) and `k ≤ n = #r` (since `k` is a valid index into `w` and `#r = #w = n`). Thus `k ≤ min(#a, #r)`.

We now have a witness for `a < r` via T1 case (i): position `k` satisfies `k ≤ min(#a, #r)`, with `aᵢ = rᵢ` for all `i < k` and `aₖ < rₖ`. By T1, `a < r`, i.e., `a < a ⊕ w`, which is equivalently `a ⊕ w > a`. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k ≤ #a` where `k` is the action point of `w`
- *Depends:* TA-Pos (PositiveTumbler) — invoked through the precondition `Pos(w)` and consumed by the action-point existence step ("The action point `k = min({i : 1 ≤ i ≤ n ∧ wᵢ ≠ 0})` exists because `Pos(w)`"); TA-Pos's positivity predicate is what guarantees `w` has at least one nonzero component for ActionPoint to find. ActionPoint (ActionPoint) — invoked to fix `k` as the first nonzero position of `w` ("the first nonzero position is `k` … `wₖ > 0` (definition of action point)") and to bound `k` against `#w` and `#a`; ActionPoint's defining minimum-position formula supplies the index used in TumblerAdd's three-region split. TA0 (WellDefinedAddition) — invoked to discharge `r = a ⊕ w ∈ T` and `#r = n` ("By TA0, `r ∈ T` with `#r = n`, so the T1 comparison between `r` and `a` is well-defined"); without TA0 the membership of `r` in T (required for T1 to apply) would be unsourced, and the result-length identity used to establish `k ≤ #r` would have no source. TumblerAdd (TumblerAdd) — invoked at the three-region computation of `r`'s components ("The TumblerAdd construction defines `r` in three regions: `rᵢ = aᵢ` for `1 ≤ i < k`, `rₖ = aₖ + wₖ`, and `rᵢ = wᵢ` for `k < i ≤ n`"), with the prefix-copy rule used in *Agreement before position k* and the advance rule used in *Strict increase at position k* to derive `rₖ = aₖ + wₖ > aₖ`. T1 (LexicographicOrder) — invoked at the closing step ("By T1, `a < r`") to convert the witness (position `k` with `aᵢ = rᵢ` for `i < k` and `aₖ < rₖ`) into the strict ordering `a < a ⊕ w` that the postcondition asserts; T1 case (i) supplies the licensing condition for the witness.
- *Postconditions:* `a ⊕ w > a`
