# Review of ASN-0116

I checked the core construction end to end: the valid-composite decomposition (K.α×n → K.μ⁻ → K.μ⁺ → K.ρ×n), the per-step precondition discharge at intermediate states, the gapped/filled bridge between ASN-0082's M'₀ and INSERT's filled M'(d), the boundary couplings J0/J1★/J1'★, and the consequence claims IP0–IP6. The rigor holds up. The two-step K.μ⁻/K.μ⁺ decomposition is correctly justified as necessary (prior-domain agreement forbids a single K.μ⁺ that rewrites relabeled suffix positions). The edge cases the rubric demands are all present and correct: empty subspace (both sub-cases a/b — the content-region-vs-arrangement-empty distinction is handled well), front insertion (J=1 with n'_{s_C}=0 strict contraction), and append (J=N+1, K.μ⁻ dropped). Internal distinctness of `A_new` — which I-ALLOC's well-definedness needs — is in fact discharged by the stepwise-freshness phrasing ("fresh against the store as it stands after the previous step"). Depth is met: consequences derived, a concrete m=2 example with provenance/coupling traces, and a genuinely non-trivial wp (IP6, containment-not-emptiness). No cross-ASN references outside the foundation set; no drift (META not warranted).

The findings below are the anti-bloat patterns the active classifier asks for, plus one citation-precision slip.

## REVISE

### Issue 1: Cross-section navigation and recap prose that does not advance reasoning

**ASN-0116, multiple sections**: The note carries `review-mode.anti-bloat`; these are the skip-past sentences.

- *Effect block intro*: "Each clause below states its postcondition and cites its foundation atomic; per-step preconditions are discharged step by step in the valid-composite section below." — pure structural narration plus a forward pointer.
- *K.μ⁻ discharge*: "the front-insertion extreme J = 1 (with n'_{s_C} = 0) is walked through concretely in the front-insertion boundary below." — embedded "see X below" pointer.
- *"The document remains one coherent sequence" opener*: "The previous section did the load-bearing work:" — back-reference framing prepended to an otherwise substantive clause (the valid-composite-implies-reachable-post-state argument should stay; the framing phrase should go).
- *"What we have established"*: "Two effects, two layers, kept clean: on the content layer INSERT is the n-fold allocation K.α with its provenance recording K.ρ, and on the arrangement layer the contraction–extension pair K.μ⁻ then K.μ⁺ realising ASN-0082's shift." — recaps the operation structure already stated verbatim in the Effect ("INSERT is the composite of n content allocations (K.α) … K.μ⁻ then K.μ⁺ … and n provenance recordings (K.ρ)"); the claim table immediately following carries the same content.

**Problem**: None of these advance the argument; each is navigation or recap that a precise reader works around. This is the forward/back-reference accretion the classifier targets — individually mild, the kind that compounds across cycles.

**Required**: Delete the forward/back-reference framing (items 1, 2, the "previous section" opener), keeping the substantive clauses. Cut the closing recap sentence or replace it with a single transition into the table.

### Issue 2 (minor): Worked-example provenance citation names the wrong invariant

**ASN-0116, "A worked insertion," provenance check**: "a_1 carried some (a_1, d) ∈ R at the pre-state (P7a there), and R ⊆ R' preserves it, so a_1 remains covered."

**Problem**: P7a (ProvenanceCoverage) gives only existence of *some* `d'` with `(a_1, d') ∈ R` — it does not pin `d' = d`. The *d*-specific record `(a_1, d) ∈ R` comes from P4★ (`Contains_C(Σ) ⊆ R`), since `a_1 = M(d)(q_1)` lies in the content-subspace range of `M(d)` and the pre-state is a composite boundary where P4★ holds. The statement is true, but the cited invariant doesn't supply the `(a_1, d)` it asserts.

**Required**: Cite P4★ for the *d*-specific record, or weaken the asserted record to "some `(a_1, d')`" (which P7a does give and which suffices for the post-state coverage conclusion via `R ⊆ R'`).

## OUT_OF_SCOPE

None. The Open Questions section already defers the natural successor topics (transclusion at a shared insertion point, concurrent insertions without a serializing authority, transclusion provenance, post-fragmentation obligations), and IP4/IP6 analyze how INSERT affects *existing* links rather than creating them, so they remain in scope.

VERDICT: REVISE
