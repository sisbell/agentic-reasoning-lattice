# Cone Review — ASN-0034/T10a (cycle 4)

*2026-04-26 04:47*

### Case `k = 0` does not discharge T4(iv) on `t'`
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing) — invariant has four conjuncts, each requiring discharge on `t'`
**ASN**: TA5a, Case `k = 0`. The case opens with "T4 requires: (i) `zeros(t) ≤ 3`, (ii) no two zeros adjacent, (iii) `t₁ ≠ 0`, (iv) `t_{#t} ≠ 0`" and closes with "T4 preserved unconditionally", but the body labels only (i) (zero-count argument), (ii) ("No new adjacencies arise"), and (iii) (sub-case split on `sig(t)`). T4(iv) on `t'` — i.e. `t'_{#t'} ≠ 0` — is never labeled.
**Issue**: Cases `k = 1` and `k = 2` both explicitly verify T4(iv) on `t'` ("boundary `t'_{#t'} = 1 ≠ 0`"), so case `k = 0` is the only case in which T4(iv) preservation is left unlabeled. The fact is implicitly available — `#t' = #t` (TA5(c)), `sig(t) = #t` (TA5-SigValid), and `t'_{sig(t)} = t_{sig(t)} + 1 ≠ 0` (the NAT-closure/NAT-zero/NAT-addcompat chain) together yield `t'_{#t'} = t'_{#t} = t'_{sig(t)} ≠ 0` — but the case body never assembles this chain into a T4(iv) discharge. The conclusion "T4 preserved unconditionally" rests on a conjunct the reader is asked to fill in.
**What needs resolving**: Add an explicit T4(iv) bullet to case `k = 0` — using `#t' = #t` from TA5(c), `sig(t) = #t` from TA5-SigValid, and the already-established `t'_{sig(t)} ≠ 0` — paralleling the boundary discharge in cases `k = 1` and `k = 2`, so that all four T4 conjuncts are individually checked off before "T4 preserved unconditionally" is asserted.

### `T4(ii)` discharge in case `k = 0` is one-line and elides the case split on `sig(t)`
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing) — T4(ii) is `(A i : 1 ≤ i < #t' : ¬(t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0))`
**ASN**: TA5a, Case `k = 0`: "No new adjacencies arise."
**Issue**: T4(ii) on `t'` is universally quantified over indices `i` with `1 ≤ i < #t'`, and discharge requires reasoning at each `i` whether (a) neither `i` nor `i + 1` equals `sig(t)`, in which case TA5(b) gives `t'ᵢ = tᵢ` and `t'ᵢ₊₁ = tᵢ₊₁` and T4(ii) on `t` discharges, or (b) one of `i`, `i + 1` equals `sig(t)`, in which case the position carries `t'_{sig(t)} = t_{sig(t)} + 1 ≠ 0` (established earlier) and the conjunction `t'ᵢ = 0 ∧ t'ᵢ₊₁ = 0` is falsified at the affected position. The one-line "No new adjacencies arise" leaves both branches unwritten. By contrast, case `k = 0`'s T4(iii) discharge is given a full split on `sig(t) = 1` vs `sig(t) ≠ 1`, so the asymmetry is internal to the same case.
**What needs resolving**: Either expand "No new adjacencies arise" into the two-branch case split that mirrors T4(iii)'s treatment in the same case (positions whose neither index hits `sig(t)`: TA5(b) + T4(ii) on `t`; positions where `i = sig(t)` or `i + 1 = sig(t)`: the `t'_{sig(t)} ≠ 0` chain falsifies the conjunction), or restate T4(ii) discharge as a direct corollary of zero-index set equality (the set of zero-positions in `t'` equals the set in `t`, and adjacency on a fixed zero-position set is invariant under that equality) with the corollary's two-line justification spelled out.

### Depends entry for T0 understates `1 ≤ #t` use sites
**Class**: REVISE
**Foundation**: T0 (CarrierSetDefinition) — supplies `(A a ∈ T :: 1 ≤ #a)`
**ASN**: TA5a, Depends list, T0 entry: "supplies `1 ≤ #t` (each tumbler has at least one component), used at case `k ≥ 3` to discharge the lower bound `1 ≤ #t + 1` for the T4(ii) instantiation index."
**Issue**: The proof body cites `1 ≤ #t` at three further sites the Depends entry omits. In cases `k = 1` and `k = 2`, the T4(iii) discharge reads "TA5(b)'s original-position agreement `(A i : 1 ≤ i ≤ #t : t'ᵢ = tᵢ)` instantiated at `i = 1` — legal since `1 ≤ #t` by T0 — gives `t'₁ = t₁`"; the legality citation of `1 ≤ #t` is direct. Symmetrically, the `sig(t) ≠ 1` sub-case of `k = 0` invokes the same TA5(b) instantiation. The Depends entry's narrowing to "case `k ≥ 3`" therefore misrepresents the dependency surface — a downstream consumer auditing which TA5a steps require T0's nonemptiness clause would not see the cases `k = 0, 1, 2` uses recorded. This is a use-site inventory gap in a structural slot, not a soundness defect in the proof body.
**What needs resolving**: Extend the T0 entry to include the cases `k = 1`, `k = 2`, and `sig(t) ≠ 1` sub-case of `k = 0` uses of `1 ≤ #t` — naming them as the legality discharge for the `i = 1` instantiation of TA5(b)'s original-position agreement — alongside the existing case `k ≥ 3` use.

VERDICT: REVISE
