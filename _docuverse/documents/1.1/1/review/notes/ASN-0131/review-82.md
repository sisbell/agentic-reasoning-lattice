# Review of ASN-0131

This is a mature, mathematically sound note. The core definition (RE-DEF), the soundness/completeness reading, the union and one-sided-intersection laws, the two intersection counterexamples (non-injective and injective), the RE-ADDR addressability derivation, and the contraction/retraction stability arguments all check out — I verified the worked instance and both counterexample arrangements for validity, and the proofs are shown rather than hand-waved. Foundation usage is consistent and no non-foundation ASN is cited. The note carries `review-mode.anti-bloat`; the findings below are accreted meta-prose and one placement defect, which compound across cycles if left.

## REVISE

### Issue 1: RE-CLIP/RE-WHOLE independence is restated three to four times

**ASN-0131, "Extent" / "A worked instance" / Claims table**: The point that no-clipping (RE-CLIP) holds under *both* readings and is orthogonal to whole-vs-touching (RE-WHOLE) is made in:
- Extent: *"RE-CLIP holds of *both*... What separates the readings is *which* spans are surfaced, not their extent, so RE-CLIP cannot decide between them."*
- Worked example: *"No-clipping holds under *either* reading of the operation: both the whole-endset and the touching-spans-only readings return this touching span unclipped."*
- Table RE-CLIP: *"universal across both the whole-endset ... and touching-spans-only ... readings, which differ only in *which* spans they surface, never in extent"*
- Table RE-WHOLE: *"not forced by RE-CLIP..."*

**Problem**: Two-plus paragraphs in different slots say the same thing in different words. The accompanying "provisional pending Open Question 1" bookkeeping is threaded through RE-DEF, RE-WHOLE, and the Extent prose, restating the same scope statement ("selection settled, return-value open") at each site.

**Required**: State the RE-CLIP ⊥ RE-WHOLE independence once (the Extent section is the right home, since it introduces both), and let the worked example *exhibit* it via the concrete `clip_W(e₁)` computation without re-asserting the general independence. Collapse the provisional bookkeeping to a single marker.

### Issue 2: RE-FIN computability paragraph is a use-site decidability inventory with a closing restatement

**ASN-0131, "The unit of the answer: anchoring without names"**: The finiteness/computability paragraph walks every test individually — *"The image I ... is constructed by deciding v ∈ W ...; coverage-membership is decidable ...; The addressability filter is decidable ... nullified(Σ) is a computable set ..."* — then closes with *"The operation therefore selects its (i, e) pairs by finitely many decidable tests over the finite store, the region's finite presentation supplying the one premise the image construction needs."*

**Problem**: The closing sentence restates the whole paragraph; the per-test enumeration is a use-site inventory. The load-bearing content is two premises (finite unconditionally from L-fin + L3; computable given decidable `v ∈ W`). Additionally, *"the SpecSet the realising FEBE operation consumes"* is an implementation-mechanics aside in a claim about an abstract guarantee.

**Required**: Trim to the two premises and the one computability hypothesis; drop the per-test walkthrough and the closing restatement. Remove or footnote the SpecSet reference — the abstract claim is "given a finitely presented W, `v ∈ W` is decidable," independent of any realising operation's input format.

### Issue 3: A reusable content-disjointness lemma is proved inside the worked example and reused as a lemma

**ASN-0131, "A worked instance" (e₃ bullet) and "Under retraction"**: The e₃ bullet carries a full general proof — separator-zero counting forcing `E(c)₁ = E(θ)₁ = s_type ≠ s_C` for any `c ∈ dom(Σ.C)` with `θ ≼ c` — establishing `coverage(e₃) ∩ dom(Σ.C) = ∅`. The retraction section then invokes it: *"the field-agreement argument used for `e₃` above is sound exactly for **unit-depth** spans ... a content `c` with `ℓ ≼ c` would force `E(c)₁ = E(ℓ)₁ = s_L ≠ s_C`."*

**Problem**: A general, reused argument lives in an illustrative slot. A worked example should *exhibit* a property and cite a lemma; here the example is load-bearing for a later proof, so the structure is backwards (proof content in an illustration slot, invoked downstream).

**Required**: Extract the fact as a named lemma — *a unit-depth span `(s, δ(1, #s))` whose start has subspace identifier `E(s)₁ ≠ s_C` has coverage disjoint from `dom(Σ.C)`* — prove it once via the field-agreement argument, and have both the worked example (for θ, `s_type`) and the retraction section (for ℓ, `s_L`) cite it. The worked example then illustrates rather than proves.

## OUT_OF_SCOPE

(none — the Open Questions already park deferred topics, including multi-store completeness (OQ5), link-subspace regions (OQ7), and the type-slot-against-content exception (OQ6), and the note correctly cites rather than rebuilds ASN-0127's image machinery and the existence/discovery taxonomy.)

VERDICT: REVISE
