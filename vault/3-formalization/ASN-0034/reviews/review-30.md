# Cone Review — ASN-0034/T10a.2 (cycle 1)

*2026-04-14 00:28*

### T10a.2 proof requires T1(c) transitivity but does not cite it

**Foundation**: T1 (LexicographicOrder), postcondition (c): transitivity — `(A a,b,c ∈ T : a < b ∧ b < c : a < c)`
**ASN**: T10a.2 (NonNestingSiblingPrefixes), proof: "By TA5(a), each application of `inc(·, 0)` produces a strictly greater tumbler under T1, so the sibling sequence is strictly increasing: `t₀ < t₁ < ... < tⱼ`. In particular `tᵢ < tⱼ`, and by T1 irreflexivity `tᵢ ≠ tⱼ`."
**Issue**: TA5(a) provides one-step strict increase: `tₙ < tₙ₊₁` for each `n`. The conclusion `tᵢ < tⱼ` for arbitrary `i < j` requires `j − i − 1` applications of T1(c) (transitivity) to chain `tᵢ < tᵢ₊₁ < ··· < tⱼ` into `tᵢ < tⱼ`. The proof cites only TA5(a) and T1(a) (irreflexivity). Transitivity is the missing bridge between "each step increases" and "distant elements are ordered." For adjacent siblings (`j = i + 1`) the step is immediate from TA5(a), but the proof is stated for arbitrary `i ≠ j`, where transitivity is load-bearing.
**What needs resolving**: The proof of T10a.2 must either cite T1(c) explicitly when concluding `tᵢ < tⱼ` for non-adjacent siblings, or reduce to the adjacent case. A formalization that supplies only TA5(a) and T1(a) as lemmas to T10a.2 will fail to close the `tᵢ < tⱼ` step.

---

### Narrative minimality claim about `inc(t, 0)` is false for non-valid addresses

**Foundation**: TA5 (HierarchicalIncrement), construction for `k = 0`: modify position `sig(t)`; TA5-SIG definition of `sig(t)`
**ASN**: Narrative after TA5 proof: "It produces the *next peer* at the same hierarchical depth — the smallest tumbler with the same length that is strictly greater than `t`."
**Issue**: The claim that `inc(t, 0)` produces the *smallest* same-length tumbler greater than `t` is false when `sig(t) < #t`. Counterexample: let `t = (2, 0, 0)`. Then `sig(t) = 1` (rightmost nonzero is position 1), so `inc(t, 0) = (3, 0, 0)`. But `(2, 0, 1)` is a same-length tumbler with `t < (2, 0, 1) < (3, 0, 0)` — it is strictly between them (T1 case (i) at position 3 for the first inequality, position 1 for the second). The minimality claim holds only when `sig(t) = #t`, i.e., when the last component is nonzero. TA5-SigValid establishes this for valid addresses satisfying T4, but the narrative asserts minimality for all tumblers without qualification. Previous findings note that TA5-SigValid is unproved; this finding adds that even with TA5-SigValid, the narrative overclaims by omitting the validity restriction. While not load-bearing for any formal property (no proof cites this claim), it will mislead a formalizer who attempts to state it as a lemma over all `T`.
**What needs resolving**: The minimality claim must be qualified: `inc(t, 0)` is the smallest same-length tumbler greater than `t` *when `sig(t) = #t`* (which holds for valid addresses by TA5-SigValid). Alternatively, state what `inc(t, 0)` actually produces in the general case: the smallest tumbler agreeing with `t` on positions `1, ..., sig(t) − 1` with a strictly larger component at position `sig(t)` and the same length.
