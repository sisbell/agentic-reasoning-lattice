Reading the ASN as a system before reporting.

**AX-1.** Well-formed axiom. Fixes the base state and explicitly names its methodological role as an induction anchor.

**AX-2.** The well-definedness argument for the domain guard on `Σ.M(d)(v)` is correctly stated. The outer `v ∈ dom(Σ'.M(d))` guards both the range occurrence of `Σ'.M(d)(v)` and the body occurrence; the text addresses only the `Σ.M(d)` side because the `Σ'` guard is structural and obvious from the formula. The scope of AX-2 — new mappings plus redirected mappings, explicitly excluding inherited ones — is correctly described and matches what S3 invokes.

**S0.** Root axiom. The formal contract correctly names its downstream consumers (S1, S3, and S5 elsewhere in the full ASN).

**S1.** Proof is a one-step consequence of S0. Correct and complete. The "S0 and S1 together establish C as an append-only log" framing is slightly loose (S0 alone supplies both monotonicity and value-immutability; S1 extracts the domain-monotonicity consequence), but the claim is sound and the phrasing is a standard label, not a false assertion.

**S3.** The induction is structurally correct: base case is vacuous by AX-1; inductive step performs an exhaustive two-way split (inherited vs. new-or-redirected) and discharges each sub-case with the right authority (J0+S1 for inherited, AX-2 for new-or-redirected). The split is logically complete — the complement of "inherited unchanged" is exactly the disjunction AX-2's range captures. The orphaned-content remark is explicitly labeled as a remark and adds historical grounding via Nelson; it is substantive, not noise.

---

### Post-proof paragraph in S3 is reviser-drift residue

**Class**: OBSERVE
**Foundation**: N/A
**ASN**: S3 (ReferentialIntegrity), paragraph beginning "It is worth saying why S1 alone does not close the argument" (after the ∎ mark)
**Issue**: The paragraph defends against a proof strategy — "S1 alone forces a ∈ dom(Σ'.C) for any mapping established by a transition" — that is not present anywhere in this ASN. The phrase "the earlier reading" names a prior misconception with no referent in the current document; it is residue from a prior review cycle's refutation, relocated into the proof body rather than dropped. The substantive content ("S3 is the join of two independent facts — S1 and AX-2 — over AX-1") is correct but belongs in an introductory motivation sentence before the proof steps, not as a post-proof explanation of why a rejected alternative fails. Under the review instructions' reviser-drift criterion, prose explaining why an axiom is needed rather than what it says is a signal of accumulated cycle noise.
**What needs resolving**: Remove the "earlier reading" sentence entirely — it has no live referent. If the "join of two independent facts" characterization is worth keeping, move it to the opening of S3's proof body as a forward-structuring sentence before the induction begins. The post-∎ position is the wrong slot for this content regardless of whether the sentence is retained.

---

VERDICT: OBSERVE