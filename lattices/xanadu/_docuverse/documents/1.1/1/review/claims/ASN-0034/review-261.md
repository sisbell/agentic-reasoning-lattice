# Cone Review — ASN-0034/TS2 (cycle 2)

*2026-04-18 08:20*

### TS2 does not discharge TA-MTO's `a ∈ T` and `b ∈ T` preconditions at the invocation site
**Foundation**: TA-MTO (ManyToOne) — preconditions `w ∈ T, Pos(w), a ∈ T, b ∈ T, #a ≥ actionPoint(w), #b ≥ actionPoint(w)` (six preconditions).
**ASN**: TS2 proof body: "We apply TA-MTO (ManyToOne) with w = δ(n, m), a = v₁, b = v₂, verifying its preconditions: (i) δ(n, m) ∈ T and Pos(δ(n, m)) … (ii) #v₁ ≥ actionPoint(δ(n, m)) and #v₂ ≥ actionPoint(δ(n, m)) …"
**Issue**: TS2 enumerates its TA-MTO precondition checks as (i) and (ii), covering four of the six TA-MTO preconditions (`w ∈ T`, `Pos(w)`, `#a ≥ actionPoint(w)`, `#b ≥ actionPoint(w)`). It never states discharges for TA-MTO's preconditions `a ∈ T` and `b ∈ T`. These transfer trivially from TS2's own preconditions `v₁ ∈ T, v₂ ∈ T`, but the per-step citation discipline sister call-site OrdinalShift applies — explicitly calling out each TA0 precondition even the trivial "First, v ∈ T by assumption" — requires that every callee precondition have a named source at the invocation site. Omitting two of six leaves those preconditions unsourced in the discharge enumeration.
**What needs resolving**: TS2's TA-MTO precondition check must enumerate discharges for all six TA-MTO preconditions, including naming the transfer of `v₁ ∈ T` and `v₂ ∈ T` from TS2's own preconditions to TA-MTO's `a ∈ T` and `b ∈ T`, matching the per-step discharge discipline OrdinalShift applies at its four TA0 preconditions.
