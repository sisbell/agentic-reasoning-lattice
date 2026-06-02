# Review of ASN-0098

## REVISE

### Issue 1: Duplicate prose restating "only the arrangement varies"
**ASN-0098, The Projection Operation**: Paragraph after the definition states "Every guarantee in this ASN follows from one observation: of the two inputs, only the arrangement varies. The endset stands still. Therefore every change in projection must be attributable to a change in `Σ.M(d)`..." The very next paragraph restates: "The definition does not separately consult `Σ.C` or `Σ.L`: the projection is sensitive only to its two inputs, and only one of them moves."
**Problem**: Two adjacent paragraphs make the identical point in different words — exactly the anti-bloat pattern flagged for this note. The second adds nothing the first did not already say.
**Required**: Delete the second paragraph; fold any residual content into the first.

### Issue 2: Redundant K.μ⁺_L paragraph in LP9
**ASN-0098, LP9**: The lemma body already states "Both K.μ⁺ and K.μ⁺_L (ASN-0047) supply (E1) and (E2) directly in their effect clauses, so the projection-level argument is identical for both," then completes the argument. A later standalone paragraph re-states: "K.μ⁺_L's effect clause `M'(d) = M(d) ∪ {v_ℓ ↦ ℓ}` ... supplies (E1) and (E2) directly, so the argument above applies unchanged."
**Problem**: The standalone paragraph duplicates the combined-case claim already discharged above. A reader following the proof must skip past it.
**Required**: Remove the redundant paragraph; the "identical for both" sentence already covers K.μ⁺_L.

### Issue 3: Duplicated canonical-restriction statement around the `tight` definition
**ASN-0098, Boundary and Width Behaviour**: Before the `tight` definition: "The achievability arguments below proceed under the canonical assumption — every span exhibited has `ℓ = δ(n, #s)` — and exhaust `F ∩ [s, s ⊕ ℓ)` by structural partition..." After it: "*Achievability.* The analysis below restricts to canonical spans, per the tight definition's canonical-form requirement above."
**Problem**: Both sentences announce the same scoping decision (restrict to canonical spans below) bracketing the definition. The second is a use-site recap that advances nothing.
**Required**: Keep one. The `tight` definition itself already carries the canonical-form requirement, so the post-definition recap is the more deletable.

### Issue 4: Motivational "why F is needed" prose in front of the F definition
**ASN-0098, Boundary and Width Behaviour**: "We formalise the 'boundary insertion does not extend the link' property against the *substrate-emittable* addresses within a span's reach rather than against raw coverage: a span includes T4-invalid zero-extensions `s.0`, `s.0.0`, … that no allocator chain can ever emit... This motivates the set `F` of substrate-emittable addresses."
**Problem**: This is "why the construct is needed" framing rather than statement of what `F` is — the kind of meta-prose the anti-bloat classifier targets. The operative content (F excludes zero-extensions; allocated addresses are chain elements) is re-derived rigorously in LP-Sub immediately below.
**Required**: Collapse to a one-line forward statement of `F`'s role, or let the formal `F` definition and LP-Sub stand on their own.

## OUT_OF_SCOPE

### Topic 1: Reverse-discovery primitive invariants
**Why out of scope**: The Open Questions correctly defer "given a V-position, return links whose projections contain it" to a future ASN; it introduces a new operation, not a gap in this one.

### Topic 2: V-order/I-order correspondence within a projection under K.μ~
**Why out of scope**: Whether projected V-order reflects underlying I-order is a genuine question, but it requires arrangement-shape machinery this ASN deliberately does not develop; properly a successor ASN.

The mathematical core is sound. LP-Fin's structural partition (`#d ≤ #d_0` bound, sub-case A separator exclusion, sub-case B's `n`-candidate count), LP12a's wp pullback, LP12b's subspace-disjointness, and the boundary cases (empty retention `R = ∅`, empty arrangement) are each carried with explicit case work and concrete worked examples. The findings above are accreted prose, not proof defects.

VERDICT: REVISE
