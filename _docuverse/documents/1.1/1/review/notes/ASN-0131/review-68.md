# Review of ASN-0131

The operation is a pure query (`Σ' = Σ`), so there is no state-mutation to check for invariant preservation; the correctness contract is the soundness/completeness biconditional, which is indeed an immediate read of RE-DEF. I verified the worked example end-to-end (the `a₄ = shift(a₂,2)` exclusive-bound reasoning, the `coverage(e₃) ∩ dom(Σ.C) = ∅` field-agreement argument, and all five touch tests), the union law and its `Avail`-factoring, the one-sided intersection law with both counterexamples (including that the *injective* one defeats `⊇`), RE-CWP and its `R = ∅` boundary, and the transition-kind enumeration in the stability section. The mathematics is sound. The findings below are one faithfulness defect in a load-bearing import and two anti-bloat instances.

## REVISE

### Issue 1: "every retraction to-set is unit-depth" overstates ASN-0086's discipline

**ASN-0131, "The unit of the answer" (standing assumption) and "Fresh emissions and the addressable population"**: "ASN-0086's *unit-depth retraction discipline* — every retraction to-set is a unit-depth span `{(t, δ(1, #t))}` at a single prior target — is the **to-set consequence** of this commitment" and "every retraction to-set in `Σ'.L` is unit-depth at some link `t ∈ dom(Σ'.L)`".

**Problem**: ASN-0086's unit-depth discipline constrains only `L_R^Σ` tuples — the *arity-3, triple-restricted* retraction slice ("every `L_R^Σ` tuple has to-endset of the form `{(b, δ(1, #b))}`"). ASN-0086 explicitly admits *higher-arity* retraction-typed links into `dom(L)` via non-Nullify `K.λ` ("a higher-arity `K.λ` at `K ~ R` enters `dom(Σ'.L)` but not `L_R`"), and these carry no unit-depth constraint. So "every retraction to-set in `Σ'.L` is unit-depth" is false in ASN-0086's model. Relatedly, the note's paraphrase of the commitment — "every store transition that adds a retraction-typed link is a `Nullify`" — strengthens ASN-0086's actual commitment ("every `→`-step with `L_R^Σ ⊊ L_R^{Σ'}` is a `Nullify`"), which governs only arity-3-slice growth.

The conclusion of RE-ADDR (a fresh output is addressable unless it is an arity-3 retraction targeting its own emitter) is nonetheless **correct**, because `nullified(Σ)`'s existential "ranges over `L_R^Σ`" — higher-arity retraction-typed links never enter it. But the argument as written rests on a universal the foundation does not grant; the antichain step is licensed only for the `L_R` to-sets that actually feed `nullified`.

**Required**: Scope the unit-depth claim to `L_R` / nullifying to-sets (which is all `nullified` consults, and is exactly what RE-ADDR needs), or explicitly adopt the stronger no-higher-arity-retraction discipline as a *local* assumption distinct from ASN-0086's commitment. Separately, note that importing the unit-depth discipline requires ASN-0086 *layer*-reachability (unit-depth is discharged "for every layer-reachable state"), whereas R0a/R-Scope are *`→*`*-reachable lemmas; the Σ.L-evolution bridge cites both uniformly as "`∀`-quantified ASN-0086 Σ.L-lemma[s]" to "every ASN-0047-reachable state" without distinguishing the two reachability strengths or noting that layer-reachability of the replayed sequence depends on the standing discipline commitment.

### Issue 2: Open Question 4 sketches its own candidate answer

**ASN-0131, Open Questions, item 4**: "...with the per-endset `touch` quantifier eliminated (for instance, a single-meet cardinality bound on each coverage against the union image together with the image-distribution gap `image(W₁) ∩ image(W₂) ⊇ image(W₁ ∩ W₂)`)?"

**Problem**: The question is fully posed by the clause before the parenthetical ("what is the weakest *structurally-restricted sufficient* condition — phrased directly on the available endsets' coverages and the three region images... with the per-endset `touch` quantifier eliminated"). The "(for instance, ...)" parenthetical volunteers a speculative answer — essay content in a structural slot, exactly the forward-reference accretion this pass targets.

**Required**: Drop the candidate-answer parenthetical.

### Issue 3: Use-site inventory closing the stability section

**ASN-0131, end of the stability discussion**: "These motions are recorded as RE-EDIT — the image under editing, with RE-CWP the exact contraction sub-case — and RE-RET, the active population under emission and retraction."

**Problem**: This sentence maps the preceding prose back onto three claim labels that are already attached at their claims and itemised in the Claims table. It advances no reasoning — a use-site inventory the precise reader skips. (The intersection section's framing — "the tempting diagnosis... names only the weaker one," "The two constructions together fix the diagnosis" — is adjacent essayistic connective tissue; the load-bearing content there is the two counterexamples and the conclusion that no arrangement restriction recovers `⊇`, which should stand without the diagnosis narration.)

**Required**: Cut the closing inventory sentence; trim the intersection-section framing to its mathematical content.

## OUT_OF_SCOPE

None. The seven Open Questions correctly defer future territory (link-subspace regions, rendered/V-position answers, cross-store completeness, the type-slot-against-content exception) without smuggling claims into the note, and the note cites ASN-0127's image/discovery machinery rather than rebuilding it.

VERDICT: REVISE
