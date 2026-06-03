# Review of ASN-0070

I checked the inverse-image definition (F0), the operation (F1), the canonical-form theorem (F-canonical), and all derived properties against the foundations. The mathematics is sound: Step 1's case split on `actionPoint(ℓ)`, Step 2's consecutivity characterisation, and Steps 3–4's existence/uniqueness construction are complete and operate on note-local objects (the V-restricted denotation, the inverse-image point-set) that no foundation covers. The worked example exercises F-sound, F-complete, F-multi, F-empty, F-contig, F-state, and the cross-subspace straddle. No correctness gaps found.

The remaining issues are accreted meta-prose (the note carries the anti-bloat classifier), concentrated around the recently-revised vacuous-subspace / empty-coverage distinction.

## REVISE

### Issue 1: Essay content in F1's Postcondition slot
**ASN-0070, F1 — FollowOperation, Postcondition**: "The empty component `Σ_V^S = ⟨⟩` is admissible from two distinct sources: (a) when `V_S(d) = ∅` ... (b) when `V_S(d) ≠ ∅` but `R(d, L(ℓ).eᵢ)|_S = ∅` ... So `Σ_V^S = ⟨⟩` does not imply the subspace is vacuous."
**Problem**: A postcondition slot should state the condition (the equation `⟦Σ_V^S⟧_V = R(d, L(ℓ).eᵢ)|_S` and the per-subspace shape). The multi-sentence (a)/(b) source analysis and the trailing defensive clarification ("does not imply the subspace is vacuous") are explanatory essay placed in a structural slot. The clarification only exists to forestall a misreading, which is meta-prose.
**Required**: Reduce the Postcondition to the equation and the admissibility of `⟨⟩`. Relocate the (a)/(b) distinction, if retained, to a single remark.

### Issue 2: Duplication of the (a)/(b) distinction across F1 and the worked example
**ASN-0070, Worked Example, Configuration 1, "Partial emptiness (not F-empty)" bullet**: "The empty component `Σ_V^{s_L}` is empty ... Note the link subspace here is *not* vacuous ... The empty component is therefore source (b) ... It is *not* a verification of F-empty, whose hypothesis ... fails here ... and whose conjunctive postcondition ... does not hold."
**Problem**: This bullet re-states, at length, the same source-(a)-vs-source-(b) distinction that F1's postcondition prose already carries (Issue 1) — two passages saying the same thing in different words. The defensive framing ("It is *not* a verification of F-empty, whose hypothesis ... fails here") works to prevent a misreading rather than to verify the configuration.
**Required**: Keep one home for the distinction. In the example, retain only the terse positive check (`R(d, e)|_{s_L} = ∅`, `⟦⟨⟩⟧_V = ∅`) and drop the comparative prose about which source applies and why it is not F-empty.

### Issue 3: F-multi's "Structural admissibility" is defensive framing
**ASN-0070, F-multi — MultiplicityPreservation, Derivation**: "The implication above derives the conclusion from the hypothesis without further assumption. What ensures the hypothesis is not vacuously satisfied is that ASN-0047's content-subspace arrangement extension K.μ⁺ imposes no injectivity constraint..."
**Problem**: The opening sentence is commentary on the proof's own structure, and the framing ("What ensures the hypothesis is not vacuously satisfied is...") justifies why the lemma is non-vacuous rather than advancing the claim. The substantive content (K.μ⁺ imposes no injectivity, unlike CL-UNIQ for the link subspace) is a fact worth keeping, but the meta-scaffolding around it is reviser-drift accretion.
**Required**: Drop the proof-structure sentence and the "not vacuously satisfied" framing. State the realisability fact directly as a one-line remark (K.μ⁺ has no content-subspace injectivity constraint, so `M(d)(v₁) = M(d)(v₂) = a` with `v₁ ≠ v₂` is reachable).

### Issue 4: Rhetorical filler in F-empty
**ASN-0070, F-empty — EmptyAdmissibility**: "There is no exception, no error, no fallback. The empty per-subspace family (V-restricted) is a regular outcome of the operation."
**Problem**: Rhetorical emphasis appended after the ∎. It restates the lemma's already-proven content without adding reasoning.
**Required**: Remove, or fold a single factual clause ("empty resolution is a normal result, not an error") into the postcondition.

## OUT_OF_SCOPE

### Topic 1: Cross-home resolution relationships (Open Question 1)
**Why out of scope**: The relationship between resolutions against documents transcluding from different home subsets is genuinely new territory, correctly deferred.

### Topic 2: Concurrency semantics of `follow` (Open Question 2)
**Why out of scope**: Concurrent-modification semantics are not part of this query's specification; belongs in a transition/concurrency ASN.

VERDICT: REVISE
