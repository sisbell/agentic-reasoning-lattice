# Review of ASN-0042

## REVISE

### Issue 1: O1a mislabeled as "AccountPrefix" in the Delegation section
**ASN-0042, Delegation**: "Delegation preserves O1a (AccountPrefix) — base: O14's third clause (`(A π ∈ Π₀ : zeros(pfx(π)) ≤ 1)`)."
**Problem**: O1a is **AccountOwnershipBoundary** (`zeros(pfx(π)) ≤ 1`). **AccountPrefix** is the distinct derived lemma `acct(a) ≼ a` in the Structural Provenance section. The parenthetical attaches the wrong nickname to O1a, conflating two different claims in the very paragraph that discharges O1a's preservation step.
**Required**: Replace `(AccountPrefix)` with `(AccountOwnershipBoundary)`.

### Issue 2: `pfx(π)` axiom introduction enumerates downstream consumers
**ASN-0042, pfx(π) (OwnershipPrefix)**: "Its codomain is constrained to valid tumblers ... so that field extraction (T4b) and the hierarchical level `zeros(pfx(π))` are determinate and the prefix comparison `pfx(π) ≼ a` of O1 is well-defined."
**Problem**: This is a definition's introduction enumerating its downstream consumers (T4b, O1) rather than advancing the definition's meaning — exactly the accretion pattern flagged. The codomain constraint is already stated in the Axiom/postcondition (b).
**Required**: Drop the consumer inventory; state the constraint once in the contract.

### Issue 3: Rationale prose around the O5 axiom
**ASN-0042, O5**: "The quantifier `a ∈ Σ'.B ∖ Σ.B` restricts O5 to transition-induced allocations: bootstrap-seeded addresses in `Σ₀.B` are governed by ASN-0040's B₀ conf., not by O5."
**Problem**: Prose around an axiom explaining *why the quantifier is scoped as it is* rather than what the axiom says — a "Scope"-style justification sub-paragraph. The quantifier is self-explanatory from the formula.
**Required**: Remove, or fold the bootstrap exclusion into the formal statement without the explanatory gloss.

### Issue 4: Repeated motif "refinement-only regime of O3 and irrevocability of O8"
**ASN-0042, OwnershipDomainPermanence corollary / O8 design-confirmation / O10 construction**: The same framing — "instantiates O3's refinement-only regime ... and the irrevocability of O8" — is asserted three times in three sections.
**Problem**: Two/three paragraphs saying the same thing in different words; compounding cross-section restatement.
**Required**: State the connection once (at O8, where it is established) and let the later sections cite it without re-narrating.

### Issue 5: Defensive exhaustiveness claim in O10(a) entailment
**ASN-0042, O10**: "This holds for both `zeros = 0` and `zeros = 1`; no case distinction is needed."
**Problem**: An exhaustiveness/reassurance claim that advances no reasoning — the biconditional already quantifies over all principals.
**Required**: Delete the sentence.

### Issue 6: Forward/backward deferral accretion
**ASN-0042, multiple sites**: "O1a is a reachable-state invariant, proved in the *Delegation* section"; worked example "delegated to `π_B` only at `Σ_2 → Σ_3` below"; "witnessed by the sub-delegation ... introduced in the O8 verification above."
**Problem**: Several paragraphs defer to the same downstream/upstream locations, the forward-reference accretion pattern this note's classifier targets. The reader must skip to resolve a claim stated here.
**Required**: Prove O1a where it is stated (or state it where proved); in the worked example, order milestones so each delegation is introduced once at its trajectory point rather than cross-pointed.

### Issue 7: O7(c) per-state-obligation prose duplicated
**ASN-0042, O7 postcondition (c) proof and Formal Contract**: The discussion that conditions (ii)/(iv) become "genuine per-state obligations beyond `Σ'`, re-checked at the prospective delegation state alongside (v)" appears in full in the proof body and is then restated in the Formal Contract postcondition.
**Problem**: Two passages in the same document saying the same thing.
**Required**: Keep the load-bearing statement in the contract; the proof body should establish it, not re-summarize it.

### Issue 8: Foundation-notation rename `s.B → Σ.B`
**ASN-0042, State Axioms**: "`Σ.B` denotes the baptismal registry ... introduced in ASN-0040 (written `s.B` there)."
**Problem**: Renaming a foundation symbol risks drift (rule 7). It is defensible here because the ownership state `Σ` carries `B` as a component, but the rename should be justified by that embedding, not presented as a free relabel.
**Required**: Either retain `s.B` for the registry component or state explicitly that `Σ.B` is the projection of ownership state `Σ` onto ASN-0040's `s.B` — one line, not a free substitution.

## OUT_OF_SCOPE

### Topic 1: Ownership transfer invariants
**Why out of scope**: The Open Questions correctly defer transfer (Nelson's "bought the document rights") to a future ASN; O3 deliberately specifies only the refinement-only regime. No error here.

### Topic 2: Cross-node identity federation
**Why out of scope**: O9 establishes node-locality; federation invariants are flagged as an open question, which is the right disposition.

VERDICT: REVISE
