# Review of ASN-0115

I checked every claim's derivation. The mathematics is sound: the Confinement lemma's T5 application is correct; R6's no-interior-hole argument correctly restricts to the bindable slice and discharges the empty-`act` sub-cases; R7's active-set agreement holds even when the consulted restriction is non-empty but depth-incompatible (the override discards it identically at both states); R8's link-vacuity follows cleanly from CL-OWN + CL-UNIQ; R11's wp decomposition (live reference + automatic store membership) is correct. The worked instances are concrete and verify against the claims. No rigor or boundary gap remains.

The findings below are all anti-bloat residue — meta-prose around the consulting-state machinery that does not advance the argument. This note carries the `review-mode.anti-bloat` classifier, and these are the patterns it targets.

## REVISE

### Issue 1: Rationale explains a vacuous firing direction of the override
**ASN-0115, "What a spec-set is, and what delivery is" (act definition)**: "The override only *bites* when the start has gone too shallow (`#s < m_S(d)`), lest it capture deeper content the citation never named; when the start is too deep (`#s > m_S(d)`) the geometric intersection is already empty by Confinement, so the override is a vacuous no-op there."

**Problem**: The first clause is load-bearing — it states *why* the override exists (a too-shallow start would otherwise capture deeper content). The second clause describes a no-op: the too-deep direction of the override changes nothing, because the geometric intersection is already empty. This is the "explaining a vacuous case" pattern — reassurance about a firing direction the definition's own geometry already handles. A reader who wants the too-deep case to be vacuous can verify it from Confinement; preempting that with a no-op explanation is accretion.

**Required**: Keep the too-shallow rationale; drop the too-deep "vacuous no-op" clause.

### Issue 2: Use-site forward references in the spec-set definition
**ASN-0115, "What a spec-set is, and what delivery is"**: (a) "it is a *consulting-state* predicate `depthcompat(ρ, Σ)`, defined below and applied inside `act`." (b) "Every spec that contributes material therefore has `S ∈ {s_C, s_L}`, the assumption the depth and item reasoning below tacitly rely on."

**Problem**: Both trailing clauses are use-site forward references that add nothing to the local statement — "defined below and applied inside `act`" inventories where `depthcompat` is consumed, and "the assumption … below tacitly rely on" announces a downstream dependency. (b) additionally *mischaracterizes* that dependency: `item`'s totality is established in the `item` definition itself, from S3★-aux applied to **active positions** — not from "every contributing spec has `S ∈ {s_C, s_L}`," which is a consequence, not a load-bearing assumption. The fact that third-subspace specs deliver nothing stands on its own; the forward-pointing tail is meta.

**Required**: State `depthcompat` and the third-subspace consequence without the "below"-pointing tails; if the dependency is worth naming, name it where the reasoning actually uses it (S3★-aux on active positions).

### Issue 3: act-definition prose previews R6
**ASN-0115, "What a spec-set is, and what delivery is" (act definition)**: "silent filtering is built in, since a named position the arrangement does not bind is simply absent from the intersection."

**Problem**: This is the substance of R6 (SilentGapFiltering) stated informally in the definition's structural slot, ahead of the formal claim. The definition slot should say what `act` *is*; the filtering behavior is R6's to assert. The gloss is essay content previewing a downstream claim.

**Required**: Let the `act` definition stand as the set-equation; drop the "silent filtering is built in" gloss, which R6 carries formally.

## OUT_OF_SCOPE

The Open Questions correctly defer inline provenance, fail-vs-partial-delivery, dangling references under relaxed S3★, channel faithfulness, and subspace-straddling spans to future ASNs — no action needed; these are not errors in this ASN.

VERDICT: REVISE
