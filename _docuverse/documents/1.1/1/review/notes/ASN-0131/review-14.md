# Review of ASN-0131

I checked the worked instance by hand, the union-distributivity and selection equalities, the RE-CWP weakest precondition, and the retraction analysis. The core formal content is sound: the biconditional definition makes soundness/completeness immediate, the `e₃`/content-disjointness field-agreement argument is rigorous, the image-union proof and the RE-SEL = `findlinks_V ∩ addressable` identity are correct, and RE-CWP correctly refines D-CWP. The findings below are one rigor gap in the retraction analysis and several instances of the accreted meta-prose the `anti-bloat` classifier targets.

## REVISE

### Issue 1: Retraction type-set content-disjointness rests on an unstated assumption and an over-reaching imposed convention
**ASN-0131, *Under retraction* / RE-RET**: "We give it by discipline, seating the designated retraction type at a dedicated element-level subspace `s_R ≠ s_C` (zeros = 3, identifier s_R), exactly as the worked instance seated θ; the field-agreement argument then transfers to each span-start of Θ and yields `coverage(Θ) ∩ dom(Σ.C) = ∅`."

**Problem**: The field-agreement argument, as proved for `e₃` and re-used for the to-set, establishes content-disjoint *coverage* only for **unit-depth (prefix-coverage)** spans — there it reduces to "`θ ≼ c ⟹ E(c)₁ = E(θ)₁`." The retraction to-set `{(ℓ, δ(1, #ℓ))}` is guaranteed unit-depth by ASN-0086's `Nullify`, so that step is rigorous. But the type-set `Θ` is an arbitrary non-empty endset; ASN-0086 does **not** confine its spans to unit depth. Seating the *span-starts* in `s_R` does not establish coverage-disjointness for a wide (non-ordinal) type span, whose half-open interval `{t : s ≤ t < s ⊕ ℓ}` need not satisfy `s ≼ t`. The load-bearing phrase "transfers to each span-start of Θ" therefore relies on an unstated confinement assumption (unit-depth, or `s_R`-subtree-confined, type spans) that the discipline as stated does not pin down. Compounding this, the construction *imposes a placement convention on the retraction type* — squarely ASN-0086's mechanics — solely to rescue the minor "net removal only" flavor; the core deduplication result (a pair drops iff `ℓ` was its sole addressable bearer) does not need it, since an added `(3, Θ)` is a different pair from the dropped `(i, e)`.

**Required**: Either state RE-RET's net-removal-only conclusion *conditionally* on `coverage(Θ) ∩ dom(Σ.C) = ∅` as a hypothesis (the honest dependency, leaving the placement to the retraction ASN), or, if the discipline is kept, state explicitly the span-shape constraint (unit-depth / `s_R`-subtree confinement) that makes "transfers to each span-start" actually yield coverage-disjointness — don't leave it implicit in "exactly as the worked instance seated θ."

### Issue 2: The "full taxonomy" recap paragraph restates the transition classification twice over
**ASN-0131, *Stability* (the paragraph beginning "The full taxonomy of what moves the answer is then:")**: the paragraph classifies every transition once, then — after "This is the complete vocabulary {...} (ASN-0047), **every member now classified:**" — re-lists the identical classification a second time ("insertion K.μ⁺ and rearrangement K.μ~ ... move it through the image; the link-subspace extension K.μ⁺_L and a link-subspace-only deletion K.μ⁻ leave the content image fixed; K.λ ... moves it through Σ.L ...; and K.α, K.δ, K.ρ ... leave it fixed").

**Problem**: This is a use-site inventory / exhaustiveness recap that says the same thing twice within one paragraph, and the same classification has already been *developed* across the three preceding per-motion paragraphs (insertion/deletion/rearrangement; other-document edits; K.μ⁺_L) and is *tabulated* a fourth time in the RE-EDIT row. The "every member now classified" / "the complete vocabulary" framing is exactly the exhaustiveness-claim pattern that degrades the argument — a reader who followed the per-motion prose gains nothing and must skip it.

**Required**: Delete the recap paragraph (the per-motion prose plus the RE-EDIT table row already carry the full classification), or collapse it to a single one-line pointer rather than a doubled re-enumeration.

### Issue 3: Non-advancing meta-prose and repeated downstream deferrals
**ASN-0131, *The region…* and *Stability***: "This first move already fixes a great deal, and we will return to it: … We hold that thought." And the display/rendered mode is deferred to Open Question 3 in two places — "the rendered mode deferred to open question 3" (rearrangement bullet) and "display-level footprint fragmentation (ASN-0082) is deferred to Open Question 3" (RE-EDIT row).

**Problem**: "We hold that thought" / "we will return to it" is rhetorical filler that advances no reasoning. The doubled OQ3 deferral is the "multiple paragraphs defer to the same downstream location" pattern. Individually small, but these are the accretions the classifier asks to be caught at source before they compound.

**Required**: Drop the filler sentence; keep a single deferral to OQ3 (the RE-EDIT-row mention suffices, or the prose one — not both).

## OUT_OF_SCOPE

The Open Questions (link-subspace regions, intersection-composability, rendered/display mode, type-slot meaningfulness against content, non-co-resident link stores) are correctly deferred rather than claimed; no out-of-scope topic is given a claim that needs reclassifying. RE-UDIST's confinement to unions (leaving intersection open) is the right boundary.

VERDICT: REVISE
