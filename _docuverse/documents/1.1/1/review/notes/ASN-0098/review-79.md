# Review of ASN-0098

The proofs here are, on the whole, rigorous — LP-Fin's finitude argument, the LP9/LP10/LP11 exact-difference formulas, and the LP12a weakest-precondition derivation all carry their cases and boundaries (empty arrangement, R = ∅, tight/non-tight frontier) explicitly. I found no mathematical gap. The findings below are accreted meta-prose, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Roadmap sentence in LP12a
**ASN-0098, LP12a (ContractionDiscoverabilityWP)**: "where `enabled(K.μ⁻[d, R])` is K.μ⁻'s applicability predicate (ASN-0047), under which the post-state `Σ' = K.μ⁻[d, R](Σ)` exists. The derivation below establishes the pullback conjunct under the standing assumption that K.μ⁻ is enabled at Σ."
**Problem**: The second sentence is a pure roadmap — it announces what the immediately-following "Derivation." paragraph will do. The section structure already conveys this; the `enabled` conjunct is defined in the first sentence and the derivation opens with "We work backward from the postcondition." The roadmap adds nothing the reader needs to follow the claim.
**Required**: Delete "The derivation below establishes the pullback conjunct under the standing assumption that K.μ⁻ is enabled at Σ." Keep the first sentence defining `enabled`.

### Issue 2: Redundant narration restating LP6 and forward-referencing LP9
**ASN-0098, "Frame Conditions"** (paragraph following the arrangement-fixing template): "Newly allocated I-addresses are invisible to projection until some subsequent K.μ⁺ adds an arrangement entry referencing them: a fresh address is not yet in any `ran(Σ.M(d))`, so it lies in no projection. Insertion as a composite (allocate + arrange) splits into a K.α step, which displaces nothing (LP6), and a K.μ⁺ step, which may add a V-position to the projection if the new V-position's I-address is in `coverage(e)` (LP9)."
**Problem**: The first sentence restates LP6 (K.α displaces nothing because a fresh address is not yet in any range). The second sentence previews LP9 — which is stated in the *next* section — narrating its content before the lemma exists. This is forward-reference accretion: the "insertion composite" framing is carried by LP6 + LP9 themselves and does not need a preview paragraph sitting between the template and LP8.
**Required**: Drop the paragraph. If the K.α/K.μ⁺ composite decomposition is wanted, fold a single clause into LP9's discussion (which already covers the transclusion/coverage-membership case) rather than previewing it here.

### Issue 3: Closing restatement in LP20
**ASN-0098, LP20 (RangeConfinement)**: "Together with the per-subspace inclusions above, this gives a complete characterisation of `{Σ.M(d)(v) : v ∈ project(e, d, Σ)}` as a partition into a content-subspace component (contained in `coverage(e) ∩ dom(Σ.C)`) and a link-subspace component (contained in `coverage(e) ∩ dom(Σ.L)`), with no other contributions."
**Problem**: The preceding two sentences already establish exhaustiveness (via S8★-aux) and disjointness (via SD/L14), which is precisely "partition." This sentence re-states that result in different words — the "two paragraphs say the same thing" pattern compressed into adjacent sentences.
**Required**: Delete the closing sentence; the exhaustive-union and disjointness sentences already deliver the partition.

## OUT_OF_SCOPE

None. The Open Questions correctly defer reverse-discovery, V-order reflection, cross-document operation comparison, link-canonical contraction, and inter-link induced discovery to future ASNs without smuggling claims into this note.

VERDICT: REVISE
