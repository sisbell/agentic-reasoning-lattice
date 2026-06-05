# Review of ASN-0115

## REVISE

### Issue 1: The "deeper positions are T1-interior" justification in R6 is false for extensions past the active frontier

**ASN-0115, §"Partial delivery" (R6 proof) and the R6 statement itself**: "Named positions of `⟦σⱼ⟧` deeper than `m_S` are unbound too, but they fall T1-interior to the active range and are harmlessly filtered out of `act`" — and in the proof body: "they fall T1-*interior* to the active range — a depth-`m_S` member `[S, 1, …, 1, k]` is bracketed below and above by its own proper extensions, which lie in `⟦σ⟧` yet never reach `dom(Σ.M(d))`".

**Problem**: Two distinct errors in this justifying step.

(a) *Not all deeper named positions are T1-interior.* A deeper extension of the **frontier** active position is a terminal overrun, not interior. This is demonstrable in the ASN's own R6 worked instance: with `V_1(d) = {[1,k]:1≤k≤4}` (`n_1 = 4`) and span `s=[1,2]`, `reach=[1,7]`, the position `[1,4,1]` is deeper than `m_S = 2`, lies in `⟦σ⟧` (`[1,4] < [1,4,1] < [1,7]`), is unbound, and satisfies `[1,4,1] > [1,4] = max(V_1(d))` — i.e. it sits *above* the entire active range, not interior to it. So the quantified claim "deeper named positions fall T1-interior to the active range" is false.

(b) *The bracketing description is incorrect.* By T1 case (ii), every proper extension `t'` of a tumbler `t` satisfies `t < t'`. A position's proper extensions are therefore all strictly T1-**greater** than it; nothing is "bracketed below" by its own proper extension. The sentence "a depth-`m_S` member is bracketed below and above by its own proper extensions" cannot hold as written.

**Required**: Drop the T1-interior argument for deeper positions. The clean, correct reason is already stated immediately above it: by S8-depth every subspace-`S` active position has depth exactly `m_S`, so any named position of depth `> m_S` is simply absent from `dom(Σ.M(d))` and filtered from `act` — no claim about T1-interiority is needed (and the false one should be removed). The no-interior-hole conclusion for the bindable slice is unaffected, but the justifying prose must be corrected.

## OUT_OF_SCOPE

(none — the ASN correctly defers single-span subspace straddling, failure semantics, inline provenance, channel faithfulness, and unbound-reference delivery to its Open Questions, and defines no claims for the listed sibling-operation topics.)

VERDICT: REVISE
