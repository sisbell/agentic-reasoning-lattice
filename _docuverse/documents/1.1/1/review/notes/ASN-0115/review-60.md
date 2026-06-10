# Review of ASN-0115

I worked through every claim. The mathematics is sound: the Confinement lemma is correctly derived from T5 + TumblerAdd; the `act` override's shallow/deep analysis is correct; R2's separation of single-state faithfulness (S2 + S3★) from cross-state permanence (S0) is precise; R6's no-interior-hole guarantee is correctly scoped to the bindable slice and proved via D-SEQ★; R7's comparability requirement is genuinely necessary, not decorative; R8's link-sub-case vacuity (CL-OWN + CL-UNIQ) and the subspace-back-from-store argument (S3★ contrapositive + SD + S3★-aux) both check out; R11's wp decomposition is right. The worked instances verify the postconditions they target. I have one finding, and it is an economy finding, not a correctness one.

## REVISE

### Issue 1: The override's "deep-case" sub-lemma derives a fact no claim consumes

**ASN-0115, §"What a spec-set is, and what delivery is"** (immediately after the `act` definition): "The override *bites* only there: the deep case `#s > m_S(d)` has an already-empty geometric intersection, so force-empty discards nothing. A bound position `v ∈ dom(Σ.M(d)) ∩ ⟦σ⟧` lies in subspace `S` … forcing `#v ≥ #s − 1 ≥ m_S(d)`. The two reconcile only at `#s = m_S(d) + 1`, where `#v = m_S(d) = #p` collapses `p ≼ v` to `v = p ≺ s`, so `v < s` (T1 case (ii)) — contradicting `v ∈ ⟦σ⟧`. Hence `dom(Σ.M(d)) ∩ ⟦σ⟧ = ∅` whenever `#s > m_S(d)`, and the override's reach is exactly the shallow case."

**Problem**: The terminal conclusion — "the override's reach is exactly the shallow case" — is load-bearing for no downstream claim. Every place that meets a depth-incompatible spec routes it through `act = ∅` *uniformly*, never distinguishing the shallow sub-case (`#s < m_S(d)`) from the deep one (`#s > m_S(d)`): R3 ("for a depth-incompatible spec it is `∅`"), R6 ("the override gives `act = ∅`, so the active range is empty"), R7 ("both take the override and `act(ρⱼ, Σ) = ∅`"), and R11 (condition (i) folds depth-compatibility into membership in `act`). The derivation is a self-contained characterization of `act` *relative to the rejected geometric-intersection alternative* — it confirms force-empty discards nothing in the deep case. That is design-comparison content, not a fact any specification claim rests on, and its multi-step prefix-collapse argument is exactly the kind of "complete the picture" derivation that accretes across cycles. A reader tracking R0–R11 must work past it for no payoff.

**Required**: Remove the derivation, or compress it to a one-sentence assertion — e.g., "the override changes nothing when `#s > m_S(d)`, since Confinement and S8-depth already force `dom(Σ.M(d)) ∩ ⟦σ⟧ = ∅` there" — and drop the explicit litigation of the geometric-intersection alternative. The genuinely load-bearing justification for force-empty (the discontinuity example, where a too-shallow start vacuums the entire subspace while its neighbour captures nothing) should remain; it answers the reviewer's "why force-empty?" The deep-case minimality check should not stand as a full sub-lemma whose result nothing uses.

## OUT_OF_SCOPE

None. The ASN stays on RETRIEVEV content delivery, correctly delivers a *reference* for link positions while deferring link-structure reading (R10), and its Open Questions are properly future-ASN material.

VERDICT: REVISE
