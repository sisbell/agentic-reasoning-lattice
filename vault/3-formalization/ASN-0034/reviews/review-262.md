# Cone Review — ASN-0034/TS2 (cycle 3)

*2026-04-18 08:26*

### TS2 does not discharge OrdinalShift's preconditions at the invocation site
**Foundation**: OrdinalShift (OrdinalShift) — preconditions `v ∈ T, n ∈ ℕ, n ≥ 1`.
**ASN**: TS2 proof body: "By OrdinalShift, the assumption rewrites as v₁ ⊕ δ(n, m) = v₂ ⊕ δ(n, m)."
**Issue**: TS2 invokes OrdinalShift twice (once at each of v₁ and v₂) to rewrite `shift(·, n) = · ⊕ δ(n, m)`, but states no per-precondition discharge at the invocation site. Under the per-step citation discipline TS2 applies extensively at its six TA-MTO preconditions — and that sister proof OrdinalShift applies at its four TA0 preconditions (even the trivial "First, v ∈ T by assumption") and at its four OrdinalDisplacement preconditions — every callee precondition requires a named source at the invocation site. TS2's three OrdinalShift preconditions (`v ∈ T`, `n ∈ ℕ`, `n ≥ 1`) transfer directly from TS2's own hypotheses, but that transfer must be stated, not left implicit. The gap appears once for v₁ and once for v₂.
**What needs resolving**: TS2 must enumerate discharges for each OrdinalShift precondition at each of the two invocations (v₁ and v₂), matching the per-step discharge discipline applied downstream at the TA-MTO invocation.

### TS2 does not discharge OrdinalDisplacement's preconditions at the invocation site
**Foundation**: OrdinalDisplacement (OrdinalDisplacement) — preconditions `n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1`.
**ASN**: TS2 proof body, precondition checks (i), (ii), (v), (vi): each cites an exported postcondition of OrdinalDisplacement (`δ(n, m) ∈ T`, `Pos(δ(n, m))`, `actionPoint(δ(n, m)) = m`) with no preceding discharge of OrdinalDisplacement's own four preconditions.
**Issue**: Citing an exported postcondition is licensed only when the callee's preconditions are satisfied at the argument `(n, m)`. Sister call-site OrdinalShift makes this explicit: "Before invoking OrdinalDisplacement at `(n, m)` we discharge its four preconditions one-for-one: `n ∈ ℕ` transfers directly…; `m ∈ ℕ` follows from T0's length operator typing…; `n ≥ 1` transfers directly…; and `m ≥ 1` follows from T0's length axiom…" TS2 consumes the same three exported postconditions at an argument `(n, m)` where `m = #v₁ = #v₂`, but states no corresponding four-precondition discharge. The facts needed (n ∈ ℕ by hypothesis; n ≥ 1 by hypothesis; m ∈ ℕ from T0's length typing `#·: T → ℕ` applied to v₁; m ≥ 1 from T0's length axiom `#a ≥ 1` applied to v₁) are all available, but are not routed to named sources at TS2's invocation site.
**What needs resolving**: TS2 must discharge each of OrdinalDisplacement's four preconditions one-for-one at the point of first citing its exported postconditions, naming the source for each (TS2 hypothesis for `n ∈ ℕ` and `n ≥ 1`; T0's length operator / length axiom applied to v₁ for `m ∈ ℕ` and `m ≥ 1`), matching the routing sister call-site OrdinalShift applies.
