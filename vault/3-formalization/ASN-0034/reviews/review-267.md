# Cone Review — ASN-0034/TS3 (cycle 3)

*2026-04-18 09:30*

### TS3's Depends list omits T0 despite multiple consumption sites
**Foundation**: T0 (CarrierSetDefinition) — supplies the length operator typing `#·: T → ℕ`, the length axiom `#a ≥ 1 for all a ∈ T`, and the carrier characterisation that each component of `a ∈ T` lies in ℕ.
**ASN**: TS3 (ShiftComposition). The binder preface explicitly cites T0 twice: "with `m ∈ ℕ` following by T0's length operator typing `#·: T → ℕ` applied to `v ∈ T`, and `m ≥ 1` following by T0's length axiom `#a ≥ 1 for all a ∈ T`". The comparison step instantiates NAT-addassoc at `m = vₘ, n = n₁, p = n₂`, which requires `vₘ ∈ ℕ` — sourced from T0's carrier characterisation applied to `v ∈ T` at position `m`. TS3's declared Depends list: "OrdinalShift, OrdinalDisplacement, NAT-closure, NAT-addcompat, NAT-order, TA0, TumblerAdd, NAT-addassoc, T3".
**Issue**: T0 does not appear in TS3's Depends list, yet the proof consumes T0 at three independent sites: (a) the binder-preface derivation `m ∈ ℕ` from `#·: T → ℕ` and `v ∈ T`, which is load-bearing for OrdinalDisplacement's `m ∈ ℕ` precondition at each of the three shift unfoldings; (b) the binder-preface derivation `m ≥ 1` from T0's length axiom, which is load-bearing for OrdinalDisplacement's `m ≥ 1` precondition at each shift; (c) the NAT-addassoc instantiation at the comparison step, which requires `vₘ ∈ ℕ` as one of NAT-addassoc's three ℕ-typing preconditions, sourced from T0's carrier characterisation of `v ∈ T` as a finite sequence over ℕ. Routing `m ∈ ℕ`/`m ≥ 1` transitively through T3 or TA0 does not satisfy the per-step citation discipline TA0's own Depends articulates ("TA0 writes T0's vocabulary directly in both its precondition and postcondition lists, so it cites T0 directly in parallel with T1..."); likewise OrdinalShift's Depends cites T0 directly for its analogous invocation-site discharges `m ∈ ℕ` and `m ≥ 1`. TS3's parallel discharges must follow the same discipline.
**What needs resolving**: TS3 must add T0 (CarrierSetDefinition) to its Depends list with the three consumption sites named, or reroute the affected steps through already-listed dependencies in a way that does not require T0's vocabulary directly.

### TS3's `vₘ ∈ ℕ` premise for NAT-addassoc is unsourced
**Foundation**: NAT-addassoc (NatAdditionAssociative) — axiom `(A m, n, p ∈ ℕ :: (m + n) + p = m + (n + p))` quantifies over `m, n, p ∈ ℕ`, so each argument's ℕ-membership is a precondition of any instantiation.
**ASN**: TS3 comparison step: "At i = m: Lₘ = (vₘ + n₁) + n₂ and Rₘ = vₘ + (n₁ + n₂). These are equal by NAT-addassoc (NatAdditionAssociative), which states `(m + n) + p = m + (n + p)` for every `m, n, p ∈ ℕ`: instantiated with `vₘ, n₁, n₂`, it yields `(vₘ + n₁) + n₂ = vₘ + (n₁ + n₂)`."
**Issue**: NAT-addassoc's three ℕ-typing preconditions at the instantiation `m = vₘ, n = n₁, p = n₂` are: `vₘ ∈ ℕ`, `n₁ ∈ ℕ`, `n₂ ∈ ℕ`. The latter two transfer directly from TS3's own preconditions. The former — `vₘ ∈ ℕ` — requires T0's carrier characterisation of `T` as finite sequences over ℕ, applied at position `m` of `v ∈ T` (with `m = #v` placing position `m` within `v`). TS3 asserts the instantiation without naming a source for `vₘ ∈ ℕ`. Under the per-step citation discipline TumblerAdd enforces at its structurally identical `aⱼ ∈ ℕ` and `aₖ ∈ ℕ` discharges (each routed through T0's carrier characterisation and the precondition `k ≤ m` placing the index within `a`), the component-typing premise must be explicit.
**What needs resolving**: TS3 must source `vₘ ∈ ℕ` from a named axiom at the comparison step (T0's carrier characterisation is the natural source, combined with the binder's `#v = m` placing position `m` within `v`), and extend its Depends list accordingly.

## Result

Cone converged after 4 cycles.

*Elapsed: 2540s*
