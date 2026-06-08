# Review of ASN-0099

## REVISE

### Issue 1: Composite-wp claims after F21 are asserted without derivation
**ASN-0099, "Persistent Discoverability (I-Side)" (paragraph following F21's two specializations)**: 
> "The contraction-then-extension composite is handled by wp composition... For the range-preserving reordering K.μ~ ... the wp degenerates to `enabled ∧ (a ∈ findlinks_V(T, d, Σ))`. For a general K.μ⁻[d, ℛ] followed by an extension K.μ⁺ ... the composite wp is *weaker* than F21's contraction wp: an extension can only restore or create discoverability that the contraction removed, never destroy more of it."

**Problem**: F21 itself is fully derived, but this trailing paragraph makes three further claims — (a) the K.μ~ wp "degenerates" to a fixed form, (b) the K.μ⁻ ; K.μ⁺ composite wp is "weaker" than F21's, (c) extension "can only restore or create ... never destroy more" — each cited to a premise (wp-composition, J3/K.μ~-RANGE, LP9) but none shown as a chain. The spec's own standard is explicit: "Derived guarantees stated without derivation ... name the premises, show the chain"; "X follows from Y + Z is not a proof, it's a claim." The "weaker than" comparison in particular is an informal set/lattice ordering on weakest preconditions that is asserted, not established. These are also unlabeled (no F-number), so they read as informal accretion blurring the boundary of the formal F21 claim.

**Required**: Either (i) promote each consequence to a labeled claim with an explicit derivation (e.g., a K.μ~ instance: show `ran(Σ'.M(d)) = ran(Σ.M(d))` via K.μ~-RANGE, then unfold `findlinks_V(T, d, ·)` to the range-meets-coverage form and conclude invariance; and for the composite, instantiate `wp(K.μ⁻, wp(K.μ⁺, Q))` and show the inclusion against F21's wp via LP9's monotone effect), or (ii) remove the paragraph as commentary on composites beyond F21's single-operation scope. As written it neither proves nor confines the claims.

## OUT_OF_SCOPE

### Topic 1: Intersection/difference algebra of the I-input
F13 and F20 give union-additivity for `findlinks` and `image`; the dual behavior under intersection and difference of I-sets (where equality fails and only inclusions hold) is not addressed. This is additional algebra, not an error in the stated additive claims, and belongs to a later composite-query treatment if needed.

### Topic 2: Combined filtered-and-scoped operation
The ASN itself notes `findlinks_filtered_scoped(C, S, Σ)` is unspecified. Correctly deferred — a future definition, not a gap here.

VERDICT: REVISE
