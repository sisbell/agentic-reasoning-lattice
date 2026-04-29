# Cone Review — ASN-0034/TA-LC (cycle 1)

*2026-04-25 23:20*

I'll review ASN-0034 as a system, looking for cross-claim issues, definition drift, and proof gaps.

After working through TA-Pos, TA0, TumblerAdd, T1, T3, ActionPoint, TumblerSub, Divergence, ZPD, TA-LC, and the NAT-* axioms, I traced the precondition chains and walked the case analyses. The proofs largely hold up: TumblerAdd's strict advancement and dominance cases are exhaustive over the (∃j < k : aⱼ > 0) split with subsequent dichotomy on aₖ; T1's trichotomy proof partitions correctly via "first divergence position" with NAT-discrete contrapositively excluding gaps; TumblerSub's Pos and actionPoint identification correctly leverage Divergence + ZPD with T1(ii) elimination of (ii-b); TA-LC's k₁ vs k₂ trichotomy properly chains NAT-cancel's summand absorption.

I have a handful of minor observations.

### ZPD Relationship-to-Divergence label collision
**Class**: OBSERVE
**ASN**: ZPD's `*Postconditions (Relationship to Divergence):*` — "In Divergence case (ii), under sub-case (β) or (γ): if the longer operand has a nonzero component beyond the shorter's last position…"
**Issue**: `(β)` and `(γ)` are ZPD's own length-trichotomy labels (selecting `L`); Divergence's case (ii) sub-cases are named `(ii-a)` and `(ii-b)`. The postcondition mixes the two labeling systems and requires the reader to cross-map. Soundness is unaffected because the mapping is unambiguous (`(β) ↔ (ii-a)` when ZPD is invoked on `(a, w)` and `(γ) ↔ (ii-b)`), but a reader chasing the chain to Divergence sees a label not defined there.

### NAT-sub Consequence-vs-axiom justification prose
**Class**: OBSERVE
**ASN**: NAT-sub strict-monotonicity and strict-positivity blocks — "is exported as a *Consequence:* rather than an additional axiom clause, because its content derives from the right-inverse together with NAT-addcompat's right order compatibility…" and the parallel paragraph for strict positivity citing NAT-discrete.
**Issue**: Meta-prose explaining the editorial choice (why this is a Consequence rather than an Axiom) sits inside the body where the technical argument lives. It does not advance the derivation; the derivation that follows is what licenses the Consequence. Pattern matches "new prose around an axiom explains why the axiom is needed rather than what it says."

### TA-LC's appeal to TA0 for action-point existence
**Class**: OBSERVE
**ASN**: TA-LC proof — "Both exist because TA0 requires Pos(x) and Pos(y), so each has at least one nonzero component."
**Issue**: `Pos(x)` and `Pos(y)` are TA-LC's own preconditions; the action points exist by ActionPoint's contract directly applied to those preconditions. The detour through TA0 is unnecessary — TA0 is invoked separately for well-definedness of `a ⊕ x` and `a ⊕ y`. Citation is technically correct but indirect.

### TumblerSub length postcondition phrasing
**Class**: OBSERVE
**ASN**: TumblerSub *Postconditions:* — "`#(a ⊖ w) = L` (the longer of `#a` and `#w`, named by NAT-order trichotomy per the Definition)"
**Issue**: "the longer of" is imprecise in sub-case (α) where `#a = #w` and neither is longer. The Definition itself handles (α) cleanly via `L = #a`; the parenthetical gloss in the postcondition does not.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 942s*
