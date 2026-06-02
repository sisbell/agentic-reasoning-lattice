# Review of ASN-0047

## REVISE

### Issue 1: J0 labelled "axiom" but used as a composite-validity filter
**ASN-0047, J0 (Allocation requires placement) and Properties Introduced table**: "J0 is an axiom of the state transition model" / "**Axiomatic** — not derived from foundation."
**Problem**: J0 cannot be simultaneously an axiom of the transition system and a clause-(2) validity constraint. ValidComposite★ uses J0 precisely to *exclude* otherwise-admissible composites: "K.α alone without an accompanying K.μ⁺ and K.ρ — is not a valid composite even though every elementary precondition holds at every intermediate state." If J0 were a genuine axiom (always true), the K.α-alone sequence could not exist; but it *does* exist as a clause-(1)-satisfying elementary sequence — it is merely not *valid*. So J0 is a definitional coupling constraint on composite validity, not an axiom of the elementary transition system. The dual labelling is contradictory and obscures which role J0 plays. (Contrast J2/J3, correctly stated as derived isolation properties, and SequentialTransitionAxiom, a genuine axiom.)
**Required**: Drop the "axiom" framing for J0; state it as an imposed coupling constraint (as J1★/J1'★ already are — "imposed (not derived)"), with the Nelson citation as motivation rather than as axiomatic ground. Reconcile the Properties table "Axiomatic" tag accordingly.

### Issue 2: Forward-reference accretion around ValidComposite★
**ASN-0047, "ValidComposite★ (forward pointer)" and downstream deferrals**: "Several statements below appeal to the validity of a composite transition before its full definition is reached. Validity is ValidComposite★, defined in *Scoped coupling constraints* below."
**Problem**: This paragraph carries no reasoning content — it exists solely to justify document ordering, the flagged forward-pointer pattern. It is compounded by repeated deferrals to the same downstream location across distinct sections: the P4★ block ("Validity of a composite transition Σ →* Σ' is ValidComposite★, defined in *Scoped coupling constraints* below"), the K.ρ/K.μ⁺ coupling-trigger preamble ("This is the coupling J1★, defined in *Scoped coupling constraints* below"), P4a's definition box, and the J1'★ derivation. Four+ sites defer to one not-yet-reached definition — the "multiple paragraphs in different sections defer to the same downstream location" pattern.
**Required**: Remove the standalone forward-pointer paragraph. Either move the ValidComposite★ definition earlier (before its first appeal) or replace the scattered deferrals with a single inline note at first use. The repeated "defined in *Scoped coupling constraints* below" tags should not recur in four sections.

### Issue 3: Duplicated temporal-scope classification prose
**ASN-0047, P4a definition box and "Extended reachable-state invariants" preamble**: P4a box: "P4a is *not* a state-local invariant... We classify it explicitly as a *trace property*..." Preamble: "Calling them 'invariants' would be misleading in the strict state-machine sense; we name them *composite-boundary properties* throughout."
**Problem**: The per-state-vs-composite-boundary distinction is explained twice in different words — once in the P4a box as a classification aside, once in the preamble as an essay on why "invariant" would mislead. The "two paragraphs say the same thing in different words" pattern. The preamble's "Calling them 'invariants' would be misleading" sentence is meta-commentary on naming, not reasoning that advances any proof obligation.
**Required**: State the temporal-scope distinction once (the preamble is the right home), and reduce the P4a box to its substantive content (the witnessing-domain definition over `{Σ₀,...,Σ_n}`), citing the preamble rather than re-explaining the classification.

### Issue 4: Defensive justification imagining precondition-excluded cases
**ASN-0047, K.μ⁻ precondition**: "The strict-subset conjunct in the characterization is essential: it is the post-state image of the constructive precondition's strict-contraction clause... and without it the identity restriction `M'(d) = M(d)` would satisfy the invariant conjuncts yet fail K.μ⁻'s effect clause."
**Problem**: This paragraph imagines the identity restriction `M'(d) = M(d)` — a case K.μ⁻'s effect clause `dom(M'(d)) ⊂ dom(M(d))` already excludes — and then explains that it would be excluded. The reasoning is circular (it defends a conjunct by positing the very state the conjunct rules out) and adds no force the effect clause does not already carry. This is the "imagines a case the precondition already excludes" pattern.
**Required**: Delete the hypothetical-identity-restriction justification; the effect clause `dom(M'(d)) ⊂ dom(M(d))` and the strict-contraction clause `(E S :: n'_S < n_S)` stand on their own. The equivalence proof in "K.μ⁻ admissible contraction shape" already discharges the strict-subset correspondence rigorously.

## OUT_OF_SCOPE

### Topic 1: Renumbering-aware interior link withdrawal
The final open question (interior `DELETEVSPAN` with compaction/renumbering) is correctly deferred — K.μ⁻ models suffix removal only, and interior-position renumbering is named-operation territory.

### Topic 2: Concurrent allocation under a shared home document
The serialization question for concurrent K.λ/K.α under one document belongs to a concurrency ASN; SequentialTransitionAxiom scopes this ASN to atomic, totally-ordered transitions.

VERDICT: REVISE
