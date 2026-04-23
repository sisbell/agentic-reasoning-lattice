**TA-PosDom (PositiveDominatesZero).** `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)` — every positive tumbler is strictly greater under T1 than every zero tumbler of any length.

*Proof.* Let `t ∈ T` with `Pos(t)` and `z ∈ T` with `Zero(z)`; we show `z < t`. Before the case analysis we extract a witnessing index `k` from `Pos(t)` directly. TA-Pos unpacks `Pos(t)` to the existential `(E i ∈ ℕ : 1 ≤ i ≤ #t : ¬(tᵢ = 0))`, so the set `S = {i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}` is nonempty; T0's commitment that the index domain `{1, …, #t}` is a subset of ℕ gives `S ⊆ ℕ`. NAT-wellorder then supplies some `k ∈ S` with `(A n ∈ S :: k ≤ n)`. Membership `k ∈ S` yields (i) `1 ≤ k ≤ #t` together with `tₖ ≠ 0`. Minimality yields (ii) `tᵢ = 0` for all `1 ≤ i < k`: such an `i` lies in `{1, …, #t}`, and if `tᵢ ≠ 0` it would sit in `S` below `k`, contradicting `(A n ∈ S :: k ≤ n)`. For (iii) `0 < tₖ`: T0 places `tₖ ∈ ℕ`; instantiating NAT-zero's disjunction `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` at `n = tₖ` and excluding the equality branch via `tₖ ≠ 0` leaves `0 < tₖ`. Unpacking `Zero(z)` gives `zᵢ = 0` for all `1 ≤ i ≤ #z`. Distinguish two cases by the relationship between `#z` and `k`.

*Case `#z ≥ k`.* For `1 ≤ i < k`, `zᵢ = 0` (from `Zero(z)`, since `i < k ≤ #z`) and `tᵢ = 0` (by (ii)), so `zᵢ = tᵢ`. The case hypothesis gives `k ≤ #z`, and (i) gives `k ≤ #t`. At `i = k`: `zₖ = 0` (from `Zero(z)`), and (iii) supplies `0 < tₖ`, so `zₖ < tₖ`. By T1 case (i) with witness `k`, `z < t`.

*Case `#z < k`.* For `1 ≤ i ≤ #z`, `i < k`, so `tᵢ = 0` (by (ii)) and `zᵢ = 0` (from `Zero(z)`), giving `tᵢ = zᵢ`. From `#z < k` and (i)'s `k ≤ #t`, NAT-order's `<`/`≤` composition yields `#z < #t`. NAT-discrete (with NAT-order) gives `m < n ⟹ m + 1 ≤ n` for `m, n ∈ ℕ`; at `m = #z, n = #t` this yields `#z + 1 ≤ #t`. By T1 case (ii) with witness `#z + 1`, `z < t`. ∎

*Formal Contract:*
- *Preconditions:* `t ∈ T`, `Pos(t)`; `z ∈ T`, `Zero(z)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#·`, component projection; commitment that the index domain `{1, …, #t}` is a subset of ℕ (used to place `S ⊆ ℕ`) and that each `tᵢ ∈ ℕ`.
  - TA-Pos (PositiveTumbler) — `Pos` and `Zero` predicate definitions; unpacks `Pos(t)` to the existential whose witnesses populate `S`.
  - NAT-wellorder (NatWellOrdering) — least-element principle applied to `S` to supply the minimal index `k`.
  - NAT-zero (NatZeroMinimum) — disjunction axiom `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` instantiated at `n = tₖ` to derive `0 < tₖ` from `tₖ ≠ 0`.
  - NAT-discrete (NatDiscreteness) — forward form `m < n ⟹ m + 1 ≤ n`, used at `m = #z, n = #t`.
  - NAT-order (NatStrictTotalOrder) — `<`/`≤` transitivity and irreflexivity used both in the least-element witness and in the case analyses.
  - T1 (LexicographicOrder) — case (i) in `#z ≥ k`, case (ii) in `#z < k`.
- *Postconditions:* `(A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)`.
