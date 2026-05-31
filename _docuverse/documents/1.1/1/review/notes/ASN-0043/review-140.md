# Review of ASN-0043

I checked the proofs of L1c (chain + CPP), FSP, FSE, L9 (both cases), PrefixSpanCoverage (both inclusions), the six-step worked example, and the L8/L10/L13 coverage derivations. The technical content is sound — I found no missing case, broken precondition, or hand-waved step in the mathematical arguments. The objections below are the meta-prose patterns the anti-bloat classifier directs me to surface.

## REVISE

### Issue 1: L5 carries provenance commentary explaining why the invariant is needed, not what it says
**ASN-0043, L5 (EndsetSetSemantics)**: "Equality of endsets is not stipulated by this invariant — it is inherited from `𝒫_fin(Span)`: since `Endset = 𝒫_fin(Span)`, two endsets are equal exactly when they have the same span members, by extensionality of finite sets. L5 adds to that inherited equality the structural restriction that no operation can distinguish two presentations of the same span collection, because no operation consults span position in the first place."
**Problem**: This is the named pattern "new prose around [an invariant] explains why the axiom is needed rather than what it says." The actual teeth of L5 — *no span-positional accessor; access is by membership `(s, ℓ) ∈ e` only* — are already stated one sentence earlier and restated one sentence later. The "inherited from `𝒫_fin` vs. L5 adds" framing is defensive boundary-drawing about the invariant's logical status, and a reader must skip past it to reach the operative content.
**Required**: State the invariant once as the prohibition on any positional accessor within an endset. Drop the inherited-equality-vs-added-restriction exposition; extensional equality follows from the type and need not be re-litigated as invariant content.

### Issue 2: L6's "structural dual of L5" paragraph is relationship essay, not L6 content
**ASN-0043, L6 (SlotDistinction)**: "L6 is the structural dual of L5. L5 forbids any positional accessor *within* an endset — span access reduces to membership, with no `e.spanⱼ` operator in the model. L6 provides one *across* endsets within a link... The two together carve out the structural primitive: at the link level, position matters; within an endset, it does not."
**Problem**: The operative content of L6 — slot index is a primitive, `Σ.L(a).eᵢ` is a positional accessor, link equality is component-wise tuple equality — is fully stated in the two preceding sentences. This paragraph restates the L5↔L6 relationship as framing essay. It re-explains L5 (already stated) to position L6 against it; that is exposition around the claim, not advancement of it.
**Required**: Keep the positional-accessor and tuple-equality statements; remove the dual-of-L5 framing paragraph. The standard-triple consequence (`(F,G,Θ) ≠ (G,F,Θ)` when `F ≠ G`) is genuine content and should stay.

## OUT_OF_SCOPE

None. The worked example's six-step extension (exercising L5 multi-span, L8 discrimination and coverage-vs-decomposition, L13) is required depth, not bloat, and should be retained.

VERDICT: REVISE
