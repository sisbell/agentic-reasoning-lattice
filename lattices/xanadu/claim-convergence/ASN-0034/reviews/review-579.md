# Cone Review — ASN-0034/TA-MTO (cycle 2)

*2026-04-26 00:02*

Reading the ASN end-to-end now.

### TumblerSub postcondition silent on the zpd-undefined branch
**Class**: OBSERVE
**ASN**: TumblerSub, *Postconditions:* slot — "a ⊖ w ∈ T, #(a ⊖ w) = L (the longer of `#a` and `#w`, named by NAT-order trichotomy per the Definition); when zpd(a, w) is defined: Pos(a ⊖ w) (TA-Pos), actionPoint(a ⊖ w) = zpd(a, w) (ActionPoint)."
**Issue**: The Definition explicitly states `a ⊖ w = [0, …, 0]` when `zpd(a, w)` is undefined, so `Zero(a ⊖ w)` is determined by construction in that branch, but the contract states no positive consequent for the undefined case — a downstream consumer must re-derive `Zero(a ⊖ w)` from the Definition rather than cite a postcondition. The Pos/actionPoint pair is conditionalized; the complementary Zero/no-actionPoint conclusion is left implicit.
**What needs resolving**: (none required — soundness is intact; flag only)

### "The longer of #a and #w" elides the equal-length case
**Class**: OBSERVE
**ASN**: TumblerSub, *Postconditions:* gloss — "#(a ⊖ w) = L (the longer of `#a` and `#w`, named by NAT-order trichotomy per the Definition)".
**Issue**: NAT-order's trichotomy presents three cases (α: `#a = #w`, β: `#a < #w`, γ: `#w < #a`); the prose "the longer of #a and #w" reads case α as if one is strictly longer, which it is not. The Definition itself handles case α correctly (`L = #a`), so soundness is intact; only the postcondition gloss is loose.
**What needs resolving**: (none required — flag only)

### TA0 ⇄ TumblerAdd duplicated postcondition citation in TA-MTO
**Class**: OBSERVE
**ASN**: TA-MTO *Depends:* — "TumblerAdd (TumblerAdd) — three-region constructive definition and result-length identity" alongside "TA0 (WellDefinedAddition) — well-definedness of `a ⊕ w` and `b ⊕ w`."
**Issue**: TA0 already exports `#(a ⊕ w) = #w` as part of well-definedness, so the "result-length identity" attribution to TumblerAdd is doubly cited. Minor — TumblerAdd remains the primary source for the constructive definition that TA-MTO actually walks, so the entry is not wrong, just overlapping.
**What needs resolving**: (none required — flag only)

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 2467s*
