# Review of ASN-0101

## REVISE

### Issue 1: P4a discharge in the D11 boundary derivation relies on a single-step argument at a multi-step composite boundary

**ASN-0101, D11, boundary derivation (inductive step) and N2**: "With the base case `Σ₀` and this single inductive step, the induction closes... P4a at `Σ'` holds by N2." and N2: "`R' = R`, and any pair `(a, d) ∈ R` witnessed at some `Σ_k` in the pre-state history remains witnessed at that same `Σ_k`... DEL records no new provenance pair, so it raises no new witnessing obligation."

**Problem**: The inductive step is over composite boundaries `B_j →* B_{j+1}`, where `B_j →* B_{j+1}` is a *multi-step* composite that may contain K.ρ steps growing `R`. The derivation re-proves P4★ and P7a inductively (correctly, from J0/J1★/`R ⊆ R'`), but discharges P4a solely "by N2." N2's argument rests on `R' = R`, which holds only for a *single isolated DEL step* — not for the composite `B_j →* B_{j+1}`, across which `R` can grow. P4a (trace-witnessing) requires every pair in `R'` to be witnessed at some composite *boundary*; a provenance pair added by an intermediate K.ρ whose content placement is then removed by a DEL step *within the same composite* would not be witnessed at `B_{j+1}` (the placement is gone) nor at any earlier boundary (the pair did not yet exist). Validity does exclude this (such a composite fails J1'★, since the added pair has no surviving content-subspace witness at `B_{j+1}`), but the derivation never invokes J1'★ to make this argument — it stops at the single-DEL "DEL cannot break P4a" claim, which does not address pairs added by the composite's non-DEL steps.

**Required**: Extend the P4a discharge at the composite boundary to account for provenance pairs added by non-DEL steps within a DEL-terminated composite. Show, via composite validity (J1'★ guaranteeing every new `(a, d) ∈ R' \ R` has a surviving content-subspace witness at the endpoint boundary `B_{j+1}`), that such pairs are witnessed at `B_{j+1}` itself — rather than citing only the single-step N2 argument whose `R' = R` premise does not hold across the composite.

### Issue 2: Wrong claim reference in the worked-example verification of D10

**ASN-0101, "A worked example", *Verification of D10***: "so `enabled(DEL[d, σ]) = true`, discharging the enabledness conjunct that each D11 wp carries; the residual equivalences exhibited below are therefore the pullback factor only."

**Problem**: The weakest preconditions being verified in this passage are D10's (discoverability wp, cardinality wp, cardinality-preservation specialisation). The enabledness conjunct `enabled(DEL[d, σ])` is a feature of the D10 wps. The text instead attributes it to "each D11 wp." D11 introduces no wp — it is the ValidComposite★ extension. The reference is simply wrong.

**Required**: Change "each D11 wp carries" to "each D10 wp carries."

### Issue 3 (anti-bloat): Defensive vocabulary-provenance prose in D11

**ASN-0101, D11**: "drawn from the extended vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`... DEL is the only addition this ASN claims; K.σ is inherited from ASN-0093."

**Problem**: The trailing sentence "DEL is the only addition this ASN claims; K.σ is inherited from ASN-0093" does not advance D11's argument — the vocabulary list already exhibits both K.σ and DEL, and DEL's atomicity is established at length in "The operation." This is accreted defensive prose (a scoping clarification about which vocabulary entry is new), the kind of residue that builds up around the vocabulary list across review cycles. It explains provenance rather than stating content.

**Required**: Remove the sentence; the list itself carries the information.

## OUT_OF_SCOPE

### Topic 1: Reconstruction / reversibility of pre-DELETE arrangement
The Open Questions correctly defer arrangement reconstruction, DELETE-then-insert recovery, orphaned-I-address rediscovery, and cross-document causal ordering to downstream versioning/operation ASNs. These are genuinely new territory, not defects in this ASN.

VERDICT: REVISE
