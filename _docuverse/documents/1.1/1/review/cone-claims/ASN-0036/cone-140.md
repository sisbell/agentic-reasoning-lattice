Reading the ASN as a whole, I traced the precondition chains across all claims, verified the case analyses in D-CTG-depth and D-SEQ, and checked the dependency bookkeeping against the convention the ASN explicitly states.

The proof chain is sound end to end. D-CTG-depth's contradiction argument (NAT-wellorder for j, T0(a) for N+1 witnesses, D-INJ + NAT-card for the pigeonhole) goes through correctly. D-SEQ's Assembly correctly packages the greatest-element induction as a from-0 NAT-induction instance and the e-map construction properly hands off to P(N). D-PRED and D-INJ are used correctly as black boxes by their consumers. The "from-1 specialization" pattern is consistently applied via the W-carrier trick in D-PRED, D-INJ, D-MIN, and D-SEQ, all with the P(0)-vacuous base and Q⁻=∅ bridge to P(1). The WLOG in D-CTG-depth is justified by the symmetry of the disagreement predicate and the witness construction.

One item for the record:

---

### D-CTG's formal axiom carries a first-class constant `1` in the inner guard that the Depends list does not directly cover

**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity, ASN-0034); V-sub (SubspaceProjection)
**ASN**: D-CTG (VContiguity), Formal Contract Axiom — the inner-quantifier guard `(A v ∈ T : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d))`; D-CTG Depends list (V-sub entry): "the extreme guards u ∈ V_1(d), q ∈ V_1(d) and the consequent v ∈ V_1(d) are membership tests against this set, each unfolding to · ∈ dom(Σ.M(d)) ∧ subspace(·) = 1"
**Issue**: The formal axiom writes the literal `1` as the text-subspace identifier in the inner-quantifier guard `subspace(v) = 1`. The ASN establishes an explicit convention — stated in V-sub's own NAT-closure entry: "neither `subspace` nor T0 exports the literal constant `1`; V-sub writes `1` as a first-class value in its own formal statement, so it is grounded here directly" — requiring that any claim writing `1` as a first-class constant in its own formal statement cite NAT-closure directly, because neither `subspace` nor T0 exports `1 ∈ ℕ` as a postcondition. D-CTG writes `subspace(v) = 1` directly in its formal axiom but omits NAT-closure from its Depends. The claim is sound: the grounding runs transitively through V-sub (which cites NAT-closure). However, D-CTG's V-sub Depends entry describes only the endpoint-membership unfolding as grounded there, not the inner guard's standalone constant, leaving the direct-grounding path implicit rather than explicit as the convention requires.
**What needs resolving**: Either add NAT-closure to D-CTG's Depends with a note that it supplies `1 ∈ ℕ` for the inner-quantifier guard `subspace(v) = 1`, or extend the V-sub Depends description to explicitly state that V-sub's naming of the text-subspace identifier as `S = 1` also grounds the inner guard's constant (not only the endpoint memberships' unfolding), restoring consistency with the convention the ASN itself establishes.

VERDICT: OBSERVE