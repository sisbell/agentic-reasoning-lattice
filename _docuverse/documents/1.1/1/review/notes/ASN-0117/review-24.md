# Review of ASN-0117

I checked the operation against its foundation (ASN-0082 contraction, ASN-0047 transition vocabulary) and re-derived the novel claims. The composite realization (K.μ⁻+K.μ⁺ for R≠∅, lone K.μ⁻ for R=∅), the ValidComposite clause-2 discharge (J0/J1★/J1'★ vacuous), the gap-closure arithmetic, the boundary cases (suffix-delete, leading-span, delete-everything, within-document sharing, cross-document transclusion), and the wp derivation all hold up. Two issues remain.

## REVISE

### Issue 1: State-subscripted coverage contradicts the foundation
**ASN-0117, P4 (LinkSurvival) and §"Link survival"**: "For every endset `e` existing in `Σ`, `coverage_{Σ'}(e) = coverage_{Σ}(e)` (DEL-LIMM + LP3★...)" and "every endset's *coverage* is unchanged across the ... transition (LP3★...)".
**Problem**: ASN-0098 defines `coverage(e)` as a *purely combinatorial property of the endset's span representation — it does not consult any state component*. For a fixed endset value `e`, `coverage(e)` is state-independent, so `coverage_{Σ'}(e) = coverage_{Σ}(e)` is either trivial or mis-typed; the state subscripts invent a state-indexed coverage the foundation explicitly disallows. The citation to LP3★ reveals the intended object: LP3★ establishes `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` — invariance of the *endset stored at link `a` slot `i`*, which is meaningful precisely because the stored value could a priori change (and L12 forbids it).
**Required**: State P4's coverage clause over link slots, `coverage(Σ'.L(a).eᵢ) = coverage(Σ.L(a).eᵢ)` for `a ∈ dom(Σ.L)`, matching LP3★ directly, and drop the state-subscripted `coverage_{Σ}(e)` notation.

### Issue 2: Duplicated range-formulation justification
**ASN-0117, §"The document remains one coherent sequence" and P5 (DocumentIsolation)**: "Stating the whole range as `ran(M'(d)) ⊆ dom(C')` would be false for any document containing a link, since its preserved link positions map into `dom(L)`... disjoint from `dom(C)`" and (in P5) "Stating the resolution as `M'(d')(v') ∈ dom(C')` for *every* `v'` would be false for any `d'` containing a link, whose `s_L` positions map into `dom(L)` — disjoint from `dom(C)` by store disjointness".
**Problem**: The same defensive observation (text positions → `dom(C)`, link positions → `dom(L)`, cannot be conflated via SD) is restated in two sections, once for `M'(d)` and once for `M'(d')`. This is the "two paragraphs in different sections say the same thing in different words" pattern the anti-bloat classifier targets — the reader works past redundant meta-justification of formulation choice.
**Required**: State the subspace-split-resolution point once (where S3★ is first invoked) and let the second site cite it rather than re-argue the SD disjointness.

## OUT_OF_SCOPE

### Topic 1: Deletions below the document origin
The first Open Question (span beginning before the first arranged position) is correctly deferred; the `J ≥ 1` precondition excludes it. Future ASN territory, not an error here.

### Topic 2: Depth > 2 deletions
DELETE inherits ASN-0082's `#p = 2` restriction. Deeper text positions are a future extension of the foundation contraction, not a gap in this ASN. The ASN is honest about the scope ("carry the depth-2 text case").

VERDICT: REVISE
