# Cross-cutting Review — ASN-0034 (cycle 2)

*2026-04-09 00:22*

I've read the entire ASN-0034 as a system, tracing every precondition chain, definition usage, divergence/zpd distinction, case analysis boundary, and dependency declaration across all 60+ properties. I verified the duplicate proofs (main and verification sections for TA1, TA3, TA4) are consistent, checked that TumblerSub's zpd is never conflated with the formal Divergence, and traced the allocation uniqueness argument through all four GlobalUniqueness cases.

### GlobalUniqueness and T9 omit T1 from declared dependencies despite direct invocation

**Foundation**: T1 (LexicographicOrder), T9 (ForwardAllocation), GlobalUniqueness
**ASN**: GlobalUniqueness property table entry declares `theorem from T3, T4, T9, T10, T10a, TA5`. T9 declares `lemma (from T10a, TA5)`. Yet:
- GlobalUniqueness Case 1 states: *"Since a < b, irreflexivity of the strict order (T1, part (a)) gives a ≠ b"* — T1(a) is invoked by name.
- T9 inductive step states: *"By transitivity of the strict order (T1(c)), tᵢ < tⱼ"* — T1(c) is invoked by name.

Compare with T8, which declares `theorem from T1, T2, T4, ...` and PartitionMonotonicity, which declares `theorem from PrefixOrderingExtension, T1, T3, ...` — both list T1 when they use it directly.
**Issue**: The declared dependency chain is broken in two places. T9 needs T1(c) transitivity for its induction to compose `tᵢ < tⱼ₋₁` with `tⱼ₋₁ < tⱼ`; without it the gap from `d` to `d+1` does not close. GlobalUniqueness needs T1 both directly (Case 1 irreflexivity) and transitively through T9. Since T9 also omits T1, neither the direct nor the transitive dependency is captured in the declared chain. A formalization following the declared "from" lists would lack T1 in scope for both properties.
**What needs resolving**: T9's declared dependencies should include T1 (used for transitivity in the inductive step). GlobalUniqueness's declared dependencies should include T1 (used for irreflexivity in Case 1, and transitively required through T9).
