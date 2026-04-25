# Cone Review — ASN-0034/TS5 (cycle 3)

*2026-04-18 14:11*

Reading TS3/TS4/TS5 as a system to find cross-cutting issues not already captured in Previous Findings.

### TS4 re-derives `Pos(δ(n, m))` while OrdinalShift cites the exported postcondition
**Foundation**: OrdinalShift's proof discharges this precondition by reading `Pos(δ(n, m))` off OrdinalDisplacement's exported postcondition ("Pos(δ(n, m)) by OrdinalDisplacement's exported postcondition `Pos(δ(n, m))`"), explicitly crediting OrdinalDisplacement with having discharged the `n ≥ 1 ⟹ n ≠ 0` promotion internally "through NAT-addcompat anchor `0 < 1`, NAT-order's defining clause + transitivity of `<` + irreflexivity".
**ASN**: TS4's first precondition check: "By OrdinalDisplacement, δ(n, m) = [0, ..., 0, n] of length m, with n at position m. Since n ≥ 1, component m is positive, so δ(n, m) is not the zero tumbler — that is, Pos(δ(n, m))." TS4's Depends likewise credits OrdinalDisplacement with "the structural form `δ(n, m) = [0, ..., 0, n]` and the positivity of its m-th component" rather than the exported `Pos(δ(n, m))` postcondition.
**Issue**: TS4 takes the harder route of its own accord: reading off the structural form and then inferring positivity from `n ≥ 1`. But this inference is exactly the `n ≥ 1 ⟹ n ≠ 0` promotion the ASN's per-step citation discipline routes through NAT-addcompat anchor + NAT-order (defining clause, transitivity, irreflexivity) — cited by OrdinalDisplacement's own proof at this site, and re-cited by the OrdinalShift component-positivity lower bound proof nearby. TS4 names none of these NAT-* axioms in its Depends and performs the step inline without citation. Two symmetric ways exist to close the gap — cite the exported `Pos(δ(n, m))` postcondition (OrdinalShift's route), or do the full per-step NAT-* discharge (OrdinalDisplacement's route) — but TS4 does neither, relying on background arithmetic for the promotion.
**What needs resolving**: TS4 must either route through OrdinalDisplacement's exported `Pos(δ(n, m))` postcondition (and adjust its Depends to cite that postcondition rather than "positivity of its m-th component"), or perform the `n ≥ 1 ⟹ n ≠ 0` promotion explicitly with the matching NAT-* citations in both proof body and Depends.

---

### TS5's worked example illustrates OrdinalShift / TS1 / TS3 rather than TS5
**Foundation**: TS5's property is `shift(v, n₁) < shift(v, n₂)` whenever `n₂ > n₁`.
**ASN**: The `*Worked example.*` block sits between TS5's proof and its Formal Contract. Its content: `shift([2,3,7], 4) = [2,3,11]` (an OrdinalShift / TumblerAdd / TA0 witness), then "For TS1: take v₁ = [2, 3, 5] < v₂ = [2, 3, 9] with n = 4. Then shift(v₁, 4) = [2, 3, 9] < [2, 3, 13] = shift(v₂, 4). ✓", then "For TS3: shift(shift([2, 3, 7], 4), 3) = shift([2, 3, 11], 3) = [2, 3, 14] = shift([2, 3, 7], 7). ✓".
**Issue**: No witness is given for TS5 itself — no pair `n₁ < n₂` with `shift(v, n₁) < shift(v, n₂)` is exhibited. The OrdinalShift computation witnesses the underlying `⊕`/displacement form, the TS1 case witnesses monotonicity in the tumbler argument, and the TS3 case witnesses composition. None of these witness TS5's monotonicity-in-shift-amount claim. Reading the ASN as a whole, a per-property worked example is expected to exhibit the property it accompanies; this one is either a leftover from an earlier version or has been attached to the wrong property.
**What needs resolving**: TS5's worked example should exhibit the TS5 property directly (a concrete `n₂ > n₁` pair with the resulting `shift(v, n₁) < shift(v, n₂)` inequality verified), or the block should be relocated to whichever property it was authored for.
