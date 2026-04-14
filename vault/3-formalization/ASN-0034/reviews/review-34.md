# Cone Review — ASN-0034/T8 (cycle 3)

*2026-04-14 02:31*

Looking at the full ASN, I note that several previous findings have been addressed in this version (the roundtrip constraints are now explicitly stated as a two-condition conjunction, the ordering guarantee is in TumblerAdd's formal contract, and T8's proof uses the simpler NoDeallocation argument). One new finding.

---

### T10a.4's T4-preservation claim is an induction with no stated base case
**Foundation**: TA5a (IncrementPreservesT4) — "`inc(t, k)` preserves T4 iff `k = 0`, or `k = 1 ∧ zeros(t) ≤ 3`, or `k = 2 ∧ zeros(t) ≤ 2`"
**ASN**: T10a.4 (T4 preservation) — "Since siblings use `inc(·, 0)` (unconditionally T4-preserving by TA5a) and child-spawning uses `k' ∈ {1, 2}` within TA5a bounds, every output of a conforming allocator satisfies T4."
**Issue**: The argument that all allocator outputs satisfy T4 is an induction: TA5a provides the step (each `inc` application preserves T4 under the stated conditions), but the base is missing. For child allocators, the base address is `inc(parent_output, k')`, which satisfies T4 if the parent's output does — this is the inductive step, not the base. The inductive chain terminates at the root allocator, whose base address must satisfy T4 for the entire chain to hold, yet T10a's axiom constrains only the *operations* allocators perform (which `k` values are permitted), not the *initial state* from which they begin. The postcondition "every output of a conforming allocator satisfies T4" is stated unconditionally, as if it follows from the operational constraints alone. It does not — it requires the additional premise that the root allocator's base address satisfies T4. Without this premise, a conforming allocator starting from a non-T4 base (say `[1, 0, 0, 3]` — adjacent zeros, degenerate parse) would produce only non-T4 outputs despite obeying every operational constraint in the axiom.
**What needs resolving**: T10a must either (a) add an explicit precondition that the allocator's base address satisfies T4 (making the inductive base explicit), or (b) add an initialization axiom constraining the root allocator's starting address, so that T10a.4's claim has a complete inductive proof.
