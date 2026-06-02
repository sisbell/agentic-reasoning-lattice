# Review of ASN-0047

I read the full transition model and checked the elementary transitions, the K.δ allocation discharge, the K.μ⁻ equivalence proof, the K.μ~ decomposition, the J0/J1★/J1'★ coupling derivations, and the eight worked examples (including the numeric tumblers). The mathematical content is sound: the per-state vs composite-boundary split is coherent, the wp-derived couplings are correctly scoped to `s_C`, the φ-bijection fork characterization correctly separates multiplicity-preservation from range equality, and the worked traces check out arithmetically. The findings below are the prose-noise patterns the `review-mode.anti-bloat` classifier asks for, plus one precision item.

## REVISE

### Issue 1: SSGU restates NodeRootedForest's cross-node argument
**ASN-0047, *Elementary transitions* (NodeRootedForest and the SSGU sub-paragraph)**: NodeRootedForest's closing sentences read "Cross-node distinctness ... is not a within-subtree GlobalUniqueness consequence; it rests on T10 (PartitionIndependence), discharged through CrossNodeAccountBase, since distinct node bases are prefix-incomparable (or nest, the case handled there)." SSGU then re-states: "cross-node distinctness (T10, ASN-0034, discharged through CrossNodeAccountBase) first excludes every event under a distinct baptised node N' ≠ N, including a nested node N' ... whose base is prefix-incomparable to or nests with N's."

**Problem**: This is the "two paragraphs say the same thing in different words" pattern. The forest structure, the T10/CrossNodeAccountBase cross-node discharge, the prefix-nesting caveat, and N-as-strong-induction-base all appear in both. SSGU's only new content is the operative conclusion "assigns `a` to exactly one allocation event within that subtree" that FrontierEquivalence/ChildSpawnFreshness consume.

**Required**: Keep the cross-node/forest reasoning in one place (SSGU, since it is the cited lemma) and reduce NodeRootedForest's last two sentences to a pointer, or vice versa. The shared argument should be stated once.

### Issue 2: Class (a) K.μ~ elaboration paragraph re-derives the Decomposition section
**ASN-0047, Class (a) verification, "*K.μ~ discharge for the arrangement-shape invariants*"**: This paragraph opens "This paragraph elaborates the K.μ~ cells whose one-line discharges appear above" and then restates LRP pointwise-link-fixity, the full-clearance K.μ⁻+K.μ⁺ realization, and the S8★/D-CTG★/D-MIN★ re-establishment — all already proved in *Decomposition of K.μ~*.

**Problem**: An explicitly meta-framed ("This paragraph elaborates...") restatement of machinery established in the dedicated section. The only non-duplicated content is the S8-fin(Σ') rider (K.μ⁻ restricts a finite set, K.μ⁺ adds finitely many) and the D-SEQ★ derivation note. Those two riders are worth keeping; the surrounding re-narration of LRP and the decomposition is not.

**Required**: Collapse to the two genuinely new facts (S8-fin(Σ') discharge independent of admissibility (i); D-SEQ★ derivation at Σ') and cite *Decomposition of K.μ~* for the rest, rather than re-deriving it.

### Issue 3: Frame statements for inherited transitions are stated three times
**ASN-0047, K.α and K.λ definitions**: Each says "with frame extended by `E' = E ∧ R' = R` (Frame convention for inherited transitions)," then immediately gives an explicit `Frame:` line repeating `E' = E; ...; R' = R`, while the *Frame convention for inherited transitions* block already establishes the same extension globally.

**Problem**: `E' = E` and `R' = R` for K.α appear in the convention block, in the parenthetical reference, and in the explicit Frame line — three statements of one fact.

**Required**: Either drop the parenthetical reference (the explicit Frame line suffices) or drop the explicit `E'/R'` conjuncts from the Frame line (the convention covers them). One statement plus the convention pointer is enough.

## OUT_OF_SCOPE

### Topic 1: Interior (renumbering) arrangement contraction
K.μ⁻ models suffix-removal only; interior `DELETEVSPAN`-style compaction-and-renumbering of surviving V-positions is not modeled. This is correctly identified as a future-ASN concern in the Open Questions (the renumbering-aware contraction question), and named operations are explicitly out of scope. No revision needed — flagging only to confirm it is not a gap in *this* ASN's primitives.

### Topic 2: Mid-stream content insertion that grows the count
Genuine middle-insertion (not replacement) requires the K.μ⁻+K.μ⁺ renumber composite because K.μ⁺ cannot shift existing mappings. This is a property of the named INSERT operation (out of scope), not of the transition primitives, which compose to achieve it. No revision needed.

VERDICT: REVISE
