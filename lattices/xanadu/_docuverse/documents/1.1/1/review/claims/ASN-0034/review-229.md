# Cone Review — ASN-0034/T10a.2 (cycle 1)

*2026-04-18 03:14*

### TA5a statement disagrees between T10a body and the TA5 table
**Foundation**: TA5a (referenced as a separate property; the ASN presents two incompatible statements of it)
**ASN**: 
- T10a justification: *"TA5a (IncrementPreservesT4), which establishes that `inc(t, k)` preserves T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`, and fails for `k ≥ 3`"*
- T10a axiom body: *"`zeros(t) ≤ 3` when `k' = 1`, `zeros(t) ≤ 2` when `k' = 2`"* (runtime precondition for child-spawning)
- Consequence 4 proof: *"the axiom restricts child-spawning to `k' ∈ {1, 2}` with the zero-count bounds of TA5a"* — plural, implying both branches have bounds
- Summary table (at end of TA5 section): *"TA5a | `inc(t, k)` preserves T4 iff `k ∈ {0, 1}`, or `k = 2 ∧ zeros(t) ≤ 2`; violated for `k ≥ 3`"*

**Issue**: The table asserts that `k = 1` preserves T4 unconditionally (`k ∈ {0, 1}` with no zero-count side condition), while every other reference to TA5a in the ASN gates `k = 1` on `zeros(t) ≤ 3`. The axiom's runtime precondition, Consequence 4's induction, and the necessity argument's analysis of the `k' = 1` component spawning all depend on the conditional version. If the table is authoritative, the axiom imposes a runtime precondition (`zeros(t) ≤ 3` at `k' = 1`) that is not needed for T4 preservation, which changes the necessity argument's status for that component; if the body is authoritative, the table misstates TA5a and downstream consumers reading only the table row will carry an incorrect T4-preservation envelope.

**What needs resolving**: The ASN must state TA5a's preservation envelope identically wherever it appears — one version of the `k = 1` condition — and the choice must be reconciled with the axiom's runtime precondition so that the zero-count bound at `k' = 1` is either a genuine T4 requirement (matching the body) or is explicitly declared as a discretionary tightening over what TA5a actually requires (matching the table).
