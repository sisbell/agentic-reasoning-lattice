# Cone Review — ASN-0034/TA5 (cycle 1)

*2026-04-25 21:25*

### TA5a Case k = 0 establishes T4(iv) implicitly without explicit labeling
**Class**: OBSERVE
**Foundation**: n/a (foundation ASN)
**ASN**: TA5a Case `k = 0`. The proof derives `t'_{sig(t)} ≠ 0` via the NAT-closure/NAT-zero/NAT-addcompat chain and notes "at `i = sig(t)` neither `tᵢ = 0` nor `t'ᵢ = 0`," then concludes "T4 preserved unconditionally." Cases `k = 1` and `k = 2` explicitly call out "boundary `t'_{#t'} = 1 ≠ 0`" for T4(iv); Case `k = 0` does not.
**Issue**: Since TA5-SigValid gives `sig(t) = #t = #t'`, the established fact `t'_{sig(t)} ≠ 0` is exactly T4(iv) for `t'`, but the proof leaves the reader to assemble that syllogism. Asymmetry with the other two cases in the same proof, where T4(iv) is named explicitly.

### TA5a Case k ≥ 3 detours through T4a where T4(ii) is directly violated
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA5a Case `k ≥ 3` and the contract's `Failure:` slot. After establishing `t'_{#t+1} = t'_{#t+2} = 0`, the proof routes the contradiction through T4a's reverse-contrapositive, framed under "the counterfactual `zeros(t') ≤ 3`" so that T4a applies. The contract's `Failure:` clause likewise mediates the failure through "T4a's field-segment framing."
**Issue**: T4(ii) instantiated at `i = #t + 1` is violated by `t'_{#t+1} = t'_{#t+2} = 0` directly, with no need to suppose `T4` holds on `t'` or to bring `T4a` into the argument. The proof eventually says exactly this ("the failing clause is T4(ii) instantiated at `i = #t + 1`"), making the T4a detour load-bearing only for the contradiction's framing, not its substance. The `Failure:` clause inherits this verbosity. The reasoning is sound; the routing is not minimal.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 1159s*
