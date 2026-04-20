# Cone Review — ASN-0034/TS2 (cycle 1)

*2026-04-18 08:06*

### TS2 uses undefined notation `δ(n, m) > 0` in place of TA-MTO's `Pos(w)` precondition
**Foundation**: TA-MTO (ManyToOne) — precondition is `Pos(w)`; and TA-Pos (PositiveTumbler) — defines `Pos(t) ⟺ (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`.
**ASN**: TS2, precondition check (i): "δ(n, m) ∈ T and δ(n, m) > 0 — by OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] with n ≥ 1 and m ≥ 1, so its m-th component is positive."
**Issue**: No order `>` on `T` is defined anywhere in the ASN; the positivity predicate on tumblers is `Pos(·)`, a named predicate, not a relation to a "zero tumbler". The justification then silently drops to component-level positivity ("m-th component is positive") which is itself a third form — neither `Pos(δ(n, m))` (existential nonzero component) nor `> 0` on `T`. TA-MTO's stated precondition is `Pos(w)`; TS2 neither writes it nor discharges it in that form. Sister call-site OrdinalShift discharges this precondition by citing OrdinalDisplacement's exported postcondition `Pos(δ(n, m))` verbatim.
**What needs resolving**: TS2 must discharge TA-MTO's precondition in the form TA-MTO states it (`Pos(δ(n, m))`), routed through OrdinalDisplacement's exported `Pos(δ(n, m))` postcondition, and must drop the undefined `δ(n, m) > 0` notation.

### TS2 precondition list omits `n ∈ ℕ`
**Foundation**: OrdinalShift — preconditions `v ∈ T, n ∈ ℕ, n ≥ 1`.
**ASN**: TS2 Formal Contract Preconditions: `v₁ ∈ T, v₂ ∈ T, n ≥ 1, #v₁ = #v₂ = m`.
**Issue**: TS2 invokes OrdinalShift ("By OrdinalShift, the assumption rewrites as v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m)"), whose preconditions explicitly require `n ∈ ℕ` (per cycles 6/7 adding this typing). TS2's preconditions list `n ≥ 1` alone and do not supply `n ∈ ℕ` as an independent typing. Under the per-step discipline OrdinalShift enforces on OrdinalDisplacement's four preconditions, TS2 must make `n ∈ ℕ` an explicit TS2 precondition (or justify why `n ≥ 1` alone transfers to `n ∈ ℕ`).
**What needs resolving**: Add `n ∈ ℕ` to TS2's precondition list, matching OrdinalShift's signature, so the OrdinalShift invocation has a named TS2-level source for every OrdinalShift precondition.

### TS2 Depends does not list TA-Pos
**Foundation**: TA-Pos (PositiveTumbler) introduces the predicate symbol `Pos(·)`.
**ASN**: TS2 Depends lists T0, OrdinalShift, OrdinalDisplacement, TA-MTO, T3 — TA-Pos absent.
**Issue**: TA-MTO's precondition consumed by TS2 is `Pos(w)`; the defining meaning of `Pos(·)` is fixed by TA-Pos. OrdinalDisplacement's postcondition `Pos(δ(n, m))` re-exports what TA-Pos defines but does not define the predicate. OrdinalShift's Depends explicitly articulates this — TA-Pos must be listed directly even when `Pos(δ(n, m))` is read off OrdinalDisplacement's exported postcondition, "so that a reviser tightening TA-Pos … has Depends-backed visibility." TS2 consumes `Pos(δ(n, m))` at the same kind of site and should follow the same discipline.
**What needs resolving**: TS2 Depends must list TA-Pos (PositiveTumbler) as the source of the predicate consumed in TA-MTO's `Pos(w)` precondition check, matching the routing OrdinalShift applies.

### TS2 does not discharge ActionPoint as the source of the `actionPoint(·)` operator
**Foundation**: ActionPoint introduces `actionPoint(·) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})`.
**ASN**: TS2 Depends omits ActionPoint; TS2 precondition check (ii) uses `actionPoint(δ(n, m)) = m` citing OrdinalDisplacement only.
**Issue**: OrdinalShift's Depends establishes that even when `actionPoint(δ(n, m)) = m` is read off OrdinalDisplacement's exported postcondition, ActionPoint must be cited directly because OrdinalDisplacement's postcondition "only fixes the value of `actionPoint(δ(n, m))`, not the defining meaning of the operator." TS2 consumes the operator at the same kind of site (TA-MTO's `#a ≥ actionPoint(w)` preconditions) and omits the ActionPoint citation.
**What needs resolving**: TS2 Depends must list ActionPoint directly for the `actionPoint(·)` operator consumed in TA-MTO's precondition (ii), matching the per-step routing OrdinalShift applies.
