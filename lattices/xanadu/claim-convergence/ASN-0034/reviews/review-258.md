# Cone Review — ASN-0034/TS1 (cycle 7)

*2026-04-18 07:46*

### OrdinalShift discharges only 2 of OrdinalDisplacement's 4 preconditions at the invocation site
**Foundation**: OrdinalDisplacement's *Formal Contract* — *Preconditions:* `n ∈ ℕ, m ∈ ℕ, n ≥ 1, m ≥ 1` (four items, after cycle-6 typing updates).
**ASN**: OrdinalShift's proof, at the OrdinalDisplacement invocation at `(n, m)`:

> "Before invoking OrdinalDisplacement at `(n, m)` we discharge its preconditions: `n ≥ 1` transfers directly from OrdinalShift's own precondition, and `m ≥ 1` follows from T0's length axiom `#a ≥ 1 for all a ∈ T` instantiated at `a = v ∈ T`, yielding `m = #v ≥ 1`."

OrdinalShift's *Depends* reiterates the same two-item discharge: "OrdinalDisplacement's own preconditions `n ≥ 1, m ≥ 1` are discharged at the invocation site: `n ≥ 1` transfers directly from OrdinalShift's own precondition, and `m ≥ 1` is discharged via T0's length axiom applied to `v ∈ T`".

TS1's *Depends* at (iii) and (v) inherits the same framing: "each of which discharges OrdinalDisplacement's preconditions `n ≥ 1, m ≥ 1` at its own call site".
**Issue**: OrdinalDisplacement's contract demands four preconditions — two ℕ-typing conjuncts (`n ∈ ℕ, m ∈ ℕ`) and two ordering conjuncts (`n ≥ 1, m ≥ 1`). OrdinalShift's proof and Depends enumerate only the ordering conjuncts, leaving the ℕ-typing preconditions undischarged at the call site. Under the per-step citation discipline this ASN enforces (TS1 enumerates TA1-strict's three membership preconditions separately rather than fusing them; TA0's four preconditions are discharged one-for-one in OrdinalShift itself), OrdinalDisplacement's four preconditions must likewise be discharged one-for-one. The gap is a direct consequence of the cycle-6 typing update to OrdinalDisplacement's Preconditions not propagating back to callers that discharge those Preconditions. A reviser reading OrdinalShift's call site cannot confirm that every OrdinalDisplacement precondition has a named source.
**What needs resolving**: OrdinalShift's proof text and Depends entry for OrdinalDisplacement must discharge all four of OrdinalDisplacement's preconditions at the invocation site — explicitly naming the source of `n ∈ ℕ` (OrdinalShift's own precondition `n ∈ ℕ`) and the source of `m ∈ ℕ` (T0's length axiom placing `m = #v ∈ ℕ` from `v ∈ T`) alongside the existing `n ≥ 1` and `m ≥ 1` discharges. TS1's *Depends* at (iii) and (v), which recites OrdinalShift's discharge of OrdinalDisplacement's preconditions, must be updated in lockstep.
