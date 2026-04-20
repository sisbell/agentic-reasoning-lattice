**TA-PosDom (PositiveDominatesZero).** `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)` — every positive tumbler is strictly greater under T1 than every zero tumbler of any length.

*Proof.* Let `t ∈ T` with `Pos(t)` and `z ∈ T` with `Zero(z)`; we show `z < t`. Since `Pos(t)`, ActionPoint applies to `t` and supplies an index `actionPoint(t)` with (i) `1 ≤ actionPoint(t) ≤ #t`; (ii) `tᵢ = 0` for all `1 ≤ i < actionPoint(t)`; (iii) `t_{actionPoint(t)} ≥ 1`. Write `k` for `actionPoint(t)`. Unpacking `Zero(z)` gives `zᵢ = 0` for all `1 ≤ i ≤ #z`. Distinguish two cases by the relationship between `#z` and `k`.

*Case `#z ≥ k`.* For `1 ≤ i < k`, `zᵢ = 0` (from `Zero(z)`, since `i < k ≤ #z`) and `tᵢ = 0` (ActionPoint (ii)), so `zᵢ = tᵢ`. The case hypothesis gives `k ≤ #z`, and ActionPoint (i) gives `k ≤ #t`. At `i = k`: `zₖ = 0` (from `Zero(z)`), and ActionPoint (iii) supplies `1 ≤ tₖ`. NAT-addcompat's `n < n + 1` at `n = 0` gives `0 < 0 + 1`; NAT-closure's `0 + n = n` at `n = 1` rewrites this to `0 < 1`. NAT-order unfolds `1 ≤ tₖ` to `1 < tₖ ∨ 1 = tₖ`; composing with `0 < 1` via NAT-order transitivity (strict disjunct) or substitution (equality disjunct) yields `0 < tₖ`. By T1 case (i) with witness `k`, `z < t`.

*Case `#z < k`.* For `1 ≤ i ≤ #z`, `i < k`, so `tᵢ = 0` (ActionPoint (ii)) and `zᵢ = 0` (from `Zero(z)`), giving `tᵢ = zᵢ`. From `#z < k` and ActionPoint (i)'s `k ≤ #t`, NAT-order's `<`/`≤` composition yields `#z < #t`. NAT-discrete (with NAT-order) gives `m < n ⟹ m + 1 ≤ n` for `m, n ∈ ℕ`; at `m = #z, n = #t` this yields `#z + 1 ≤ #t`. By T1 case (ii) with witness `#z + 1`, `z < t`. ∎

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `Pos(t)`; `z ∈ T`, `Zero(z)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`, component projection.
  - TA-Pos (PositiveTumbler) — `Pos` and `Zero` predicate definitions.
  - ActionPoint (ActionPoint) — supplies `actionPoint(t)` and postconditions (i)–(iii) used as the T1 witness and agreement data.
  - NAT-wellorder (NatWellOrdering) — transitive through ActionPoint's least-element construction.
  - NAT-zero (NatZeroMinimum) — transitive through ActionPoint's postcondition (iii).
  - NAT-addcompat (NatAdditionOrderAndSuccessor) — `n < n + 1` at `n = 0`.
  - NAT-closure (NatArithmeticClosureAndIdentity) — additive identity `0 + n = n` at `n = 1`.
  - NAT-discrete (NatDiscreteness) — contrapositive form `m < n ⟹ m + 1 ≤ n`.
  - NAT-order (NatStrictTotalOrder) — `≤` unfolding, `<`/`≤` transitivity, trichotomy, irreflexivity.
  - T1 (LexicographicOrder) — case (i) in `#z ≥ k`, case (ii) in `#z < k`.
- *Postconditions:* `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)`.
