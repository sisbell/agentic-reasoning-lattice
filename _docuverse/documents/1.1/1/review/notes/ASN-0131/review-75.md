# Review of ASN-0131

This note is, on its mathematics, very strong. I checked the proofs and could not break them: RE-ADDR's nullifier analysis is sound (and correctly excludes self-retraction), RE-UDIST-∩'s injective and non-injective counterexamples both genuinely refute `⊇`, the necessary-and-sufficient touch-implication condition is right, RE-CWP's weakest precondition is correctly derived as the per-endset refinement of D-CWP, the worked instance exercises every distinctive postcondition and computes correctly, and the self-retraction edge case in RE-BND is handled with precision. Soundness/completeness as immediate reads of the biconditional are legitimately one-step. The `W ⊆ s_C` obligation is threaded carefully through every guarantee that needs it.

The note carries the anti-bloat classifier, and that is where the findings lie: a small amount of accretion has settled around the ASN-0086 import, plus one over-stated computability claim. None is a logical error; all are refinements.

## REVISE

### Issue 1: Defensive higher-arity-retraction digression re-derives a definitional fact for a non-arising case
**ASN-0131, "Fresh emissions and the addressable population"**: "Higher-arity retraction-typed links — admitted to `dom(Σ'.L)` by ordinary `K.λ` but, lacking arity 3, never entering `L_Θ` — therefore never enter `nullified`, and so bear on addressability at no arity; this is what lets RE-ADDR hold for an output of *any* arity."

**Problem**: This re-derives a definitional fact — ASN-0086's `L_Θ` *is* the arity-3 type-Θ slice, so higher-arity links are excluded by construction — and applies it to a scenario the note never produces. The note's retractions are arity-3 Nullify outputs; its non-retraction emissions are not type Θ at all, so their addressability never turns on the arity-vs-`L_Θ` interaction this sentence guards against. The main RE-ADDR argument already settles the matter on different grounds (pre-existing `L_Θ` tuples target `dom(Σ.L)`; fresh `ℓ_new ∉ dom(Σ.L)`). Tracing every use of the "at every arity" qualifier (RE-RET's emitter `b` is arity 3; RE-EDIT's and RE-UDIST-∩'s `ℓ_new`/`ℓ_e`/`ℓ_{ab}` are non-retraction, addressable because *not type Θ*, independent of arity), the higher-arity-retraction justification is never actually invoked.

**Required**: Drop the higher-arity-retraction sentence. If "at every arity" is retained, it follows for non-retraction emissions directly from their not being type Θ — state that, not the `L_Θ`-arity digression.

### Issue 2: Use-site inventory of imported ASN-0086 facts duplicates the in-proof citations
**ASN-0131, "Fresh emissions and the addressable population"**: "Under it, the addressability results import three ASN-0086 facts: every `L_Θ` to-set is a unit-depth span `{(t, δ(1, #t))}` at a single prior target ...; `dom(Σ.L)` is a prefix-antichain (R0a, FlatLinkDomain, ASN-0086); and a single `Nullify` contributes exactly its target to the nullified set (R-Scope, SingleTupleScope, ASN-0086)."

**Problem**: Each of these three facts is re-stated and re-cited at its actual point of use — unit-depth in the RE-ADDR nullifier analysis ("every `L_Θ^{Σ'}` to-set is unit-depth at some link `t`…"), R0a in the same paragraph, and R-Scope in the RE-RET single-target argument ("`{t : ℓ ≼ t} ∩ dom(Σ'.L) = {ℓ}`"). The upfront inventory previews a toolkit that is fully cited where it is consumed; it is read once and then re-encountered at each use. (The `Σ.L`-evolution bridge prose around it is *not* in this category — it is load-bearing, justifying that ASN-0086's `→*`-reachable lemmas apply across to ASN-0047-reachable states, and correctly distinguishes which lemma needs layer-reachability. Keep that.)

**Required**: Cite each ASN-0086 fact at its point of use; remove the preview inventory sentence.

### Issue 3: "Computable object" over-states what is established; finiteness holds but computability needs a decidable `W`
**ASN-0131, "The unit of the answer: anchoring without names"**: "The answer just defined is a finite, computable object."

**Problem**: Finiteness is unconditional — the answer is drawn from the finite pool `Avail(Σ)`. Computability is not: to compute `image(W, d, Σ) = {Σ.M(d)(v) : v ∈ W ∩ dom(Σ.M(d))}` one must decide `v ∈ W` for each `v ∈ dom(Σ.M(d))`, and the note pins `W` down only as "`W ⊆ T` ... typically the V-positions of a span." The decidability paragraph that follows discharges the touch test (finite image, T2/T12 coverage-membership) and the addressability filter (computable `nullified`, finite `dom(Σ.L)`), but not the image construction itself — that step silently assumes `W`-membership is decidable.

**Required**: Either constrain `W` to a finitely-presented / effectively-decidable form (e.g., the V-positions of a span, which the prose already gestures at), or state the `W`-decidability premise the computability claim rests on. Finiteness needs no such premise and can be asserted unconditionally.

## OUT_OF_SCOPE

### Link-subspace regions, rendered answers, type-slot/content matches, multiplicity, cross-store completeness
These are correctly deferred to Open Questions 1–7 rather than smuggled in. The `W ⊆ s_L` case (OQ7), the V-order-rendered answer (OQ3), the `coverage(Θ) ∩ dom(Σ.C) ≠ ∅` exception (OQ6), and multiplicity-preservation (OQ2) are genuine future territory, not gaps in this note. The note also correctly *cites* ASN-0127's image machinery and existence/discovery taxonomy rather than rebuilding them, and stays a pure-query specification (abstract guarantees an alternative implementation would have to meet) without drifting into FEBE mechanics — no META concern.

VERDICT: REVISE
