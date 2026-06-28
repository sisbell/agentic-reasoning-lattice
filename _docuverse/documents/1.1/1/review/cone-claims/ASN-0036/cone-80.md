Reading the foundation statements and the ASN claims to check for missing contracts, ungrounded steps, and cross-claim precondition gaps.

---

The proofs of D-CTG-depth are sound on close reading. The pinning argument for k = j is watertight: agreement at 1...j−1 eliminates k < j; the T1 agreement clause covers i = j when k > j, contradicting j's disagreement-set membership; so k = j and u_j < x_j follows from clause (i). The intermediate witness w satisfies all D-CTG guards: #w = m (by construction), subspace(w) = w₁ = u₁ = 1 (since j ≥ 2), zeros(w) = 0 (components 1...j copied from u, all > 0 by S8a; component j+1 is n > u_{j+1} ≥ 1; components j+2...m set to 1). The w < x direction uses T1 clause (i) at k = j with agreement at positions 1...j−1, and w_j = u_j < x_j. The infinite-sequence argument: T0(a) iterated at t = u, i = j+1 with increasing bounds yields a strictly increasing sequence n₁ < n₂ < ..., each giving a distinct w_k ∈ V_1(d) by T3, contradicting S8-fin. S8-fin, S8a, S8-depth, V-sub, subspace, and Σ.M(d) are each formally sound as stated.

One structural gap stands out.

---

### D-CTG carries no epistemic status label and no Formal Contract section

**Class**: REVISE
**Foundation**: S8-fin (FiniteArrangement), S8a (ArrangementDomainRestriction), S8-depth (FixedDepthVPositions) — cited for comparison of how posits are handled in this ASN
**ASN**: D-CTG (VContiguity) — the entire claim body
**Issue**: Every other design posit in this ASN declares itself explicitly. S8-fin's Formal Contract opens "*Axiom:* ... This is a design requirement on every reachable state. We posit it rather than derive it." S8a says "This is a protocol design posit on the class of permitted arrangements: it is accepted within this ASN without proof." S8-depth's body says "We adopt S8-depth as a *design constraint* on the arrangement — a per-subspace posit, asserted by fiat." D-CTG has none of this. It states a formal quantification over V_1(d) and a Depends list, but no Formal Contract section, no axiom or postcondition clause, and no sentence declaring whether the property is asserted or derived. Yet D-CTG-depth calls it "the contiguity axiom" and treats it as a load-bearing posit in its Depends entry. The absence is structurally significant: D-CTG's Depends list cites only definitional foundations (T0, T1, T4, V-sub, subspace) — no state-transition axioms such as AX-1, AX-2, S0–S3. A contiguity property over dom(Σ.M(d)) cannot be derived from purely mathematical foundations without transition-level axioms, so D-CTG must be a posit. But a formalization tool reading the claim text encounters only a formal statement with no proof and no explicit posit declaration — it cannot determine whether D-CTG is a theorem to discharge or an axiom to accept.
**What needs resolving**: Add a Formal Contract section to D-CTG with an explicit Axiom clause and a posit declaration matching the pattern of S8-fin and S8a. The declaration should state that D-CTG is a protocol design constraint on the class of permitted arrangements, accepted without derivation, and not a consequence of AX-1, AX-2, or the content-stream invariants S0–S3. The state-level scope (for every reachable Σ) should also be made explicit in the Axiom clause, since D-CTG's formal statement uses the shorthand V_1(d) — which hides the Σ dependence — while S8-fin and S8a spell out "for every reachable state Σ and every document d."

---

VERDICT: REVISE