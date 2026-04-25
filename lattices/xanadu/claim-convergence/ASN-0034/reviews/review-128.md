# Cross-cutting Review — ASN-0034 (cycle 1)

*2026-04-17 07:13*

### Missing or incomplete Depends clauses in T10a.1, T10a.2, T10a.3
**Foundation**: (foundation ASN; internal consistency review)
**ASN**: T10a.1 (UniformSiblingLength), T10a.2 (NonNestingSiblingPrefixes), T10a.3 (LengthSeparation) — the three T10a corollaries stated between T10a-N and T10a.4.
**Issue**: These three sub-properties have Depends clauses that do not match what their proofs invoke, breaking the per-step citation convention applied in neighboring properties (T10a.4, T10a.5, T10a.6, T10a.7, and T10a itself each enumerate every cited lemma).
- **T10a.1**: the Formal Contract has no Depends field at all, yet the proof invokes TA5(c) (`#inc(t, 0) = #t`) to discharge the inductive step.
- **T10a.2**: Depends lists only T10a.1 and Prefix, but the proof also invokes TA5(a) for the per-step strict monotonicity `inc(·, 0) > t`, T1(c) for transitivity across non-adjacent siblings (`j − i − 1` applications are named explicitly), and T1(a) for irreflexivity to conclude `tᵢ ≠ tⱼ`.
- **T10a.3**: the Formal Contract has no Depends field, yet the proof invokes T10a.1, TA5(c), TA5(d), and T3.

**What needs resolving**: Bring the three Formal Contracts into line with the per-step citation convention enforced elsewhere in the ASN (T0's introductory sentence states this policy explicitly). Either add the missing citations to Depends, or mark the properties as exempt from the convention with a visible reason. The gap matters because a reviser tightening TA5, T1, or T3 loses Depends-backed visibility into these three consequences — and because T9, GlobalUniqueness, PartitionMonotonicity, and T10a.4–T10a.7 all transitively rely on them.

### T10a misattributes the origin of `zeros(·)` to TA5a
**Foundation**: (foundation ASN)
**ASN**: T10a's axiom text and narrative reads "where `zeros(·)` is the zero-count function defined in TA5a", repeated in the "Justification" paragraph as "The axiom borrows `zeros(·)` from TA5a as a precondition symbol". The Depends entry for TA5a likewise says "supplies … the `zeros(·)` symbol the axiom names in its precondition".
**Issue**: `zeros(·)` is defined in T4 ("Define `zeros(t) = #{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}`, the count of zero-valued components in `t`"). TA5a itself opens by restating and explicitly cites T4 as the definition site: "Let `zeros(t) = … (defined in T4)." The Vocabulary entry also attributes the definition extensionally, noting use in TA5a and T10a but not a definition. T10a therefore names the wrong origin.
**What needs resolving**: T10a should cite T4 as the definition site for `zeros(·)` and (if TA5a is still wanted in Depends) explain what TA5a supplies beyond the symbol — for instance, the preservation bounds that T10a adopts as runtime preconditions. Otherwise a future tightening of the `zeros(·)` definition in T4 would fail to flag T10a through the Depends graph.
