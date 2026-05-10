# Regional Review — ASN-0034/T10a (cycle 1)

*2026-04-23 03:03*

### NAT-sub in T10a.3 Depends list is unused

**Class**: OBSERVE
**Foundation**: T10a.3 (Length separation)
**ASN**: T10a.3 Postcondition Depends list — `NAT-sub (closure and right-telescoping for the subtraction form)`
**Issue**: The proof of Consequence 3 as written uses only additive reasoning: `TA5(d)` gives `#inc(t, k') = #t + k'`, NAT-addcompat's strict successor and left order-compatibility chain `1 ≤ k' ⟹ #t + 1 ≤ #t + k'`, and the nesting-level claim is stated as additive (`m + k'₁ + … + k'_d`). No subtraction `#child − #parent` appears in the proof or the postcondition body. The NAT-sub entry in Depends appears to be drift, possibly relocated from an earlier revision.

### T4a cited in TA5a Depends but not used in the proof

**Class**: OBSERVE
**Foundation**: TA5a (IncrementPreservesT4)
**ASN**: TA5a Depends — `T4a (SyntacticEquivalence) — bridges T4's positional conditions with the non-empty-field-segment reading, supporting the case k ≥ 3 interpretation that adjacent zeros create an empty field.`
**Issue**: The case `k ≥ 3` argument instantiates T4(ii) directly at `i = #t + 1`, obtaining `¬(0 = 0 ∧ 0 = 0)`. It never invokes the non-empty-field-segment reading or any T4a-bridged equivalence. The Depends entry explains why T4a *might* be relevant rather than citing a step where it is used — the bridge is not exercised.

### "By the reverse direction of T3" in T10 proof is a minor misattribution

**Class**: OBSERVE
**Foundation**: T10 (PartitionIndependence) proof
**ASN**: `Hence aₖ = p₁ₖ ≠ p₂ₖ = bₖ. By the reverse direction of T3, a ≠ b.`
**Issue**: T3 (as cited) says equal-length tumblers agreeing on all components are equal; its contrapositive concerns *equal-length* tumblers differing in some component. Here `a` and `b` need not have equal length, and the step `aₖ ≠ bₖ ⟹ a ≠ b` follows from indiscernibility of equality (if `a = b` then `aₖ = bₖ`) rather than from T3. The conclusion is correct; the citation is stronger than needed.

### T10a.5 base-case relabeling is implicit WLOG

**Class**: OBSERVE
**Foundation**: T10a.5 (Cross-allocator prefix-incomparability) proof
**ASN**: `If tₓ = tᵧ and k'ₓ ≠ k'ᵧ: take k'ₓ = 1, k'ᵧ = 2.`
**Issue**: The proof names one arrangement of the pair without stating WLOG. The symmetric sub-case `k'ₓ = 2, k'ᵧ = 1` is covered only by implicit relabeling, and the subsequent inductive step (`When j = #bₓ`) is tied to the chosen orientation. The argument is correct under relabeling, but the WLOG step is not called out.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 292s*
