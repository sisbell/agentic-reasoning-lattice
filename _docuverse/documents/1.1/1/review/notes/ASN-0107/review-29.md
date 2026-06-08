# Review of ASN-0107

The technical content is sound. I checked `sat`/`match`/`num` for well-definedness and totality, the existence laws (E1–E4) against permanence and monotonicity, the discovery laws (D1–D3) against the K.μ family's frame and bijection equations, the R-laws against PerSubspaceContractionScope, and the R6 weakest-precondition derivation against L12/L12a and the contraction effect — all hold. The worked instance correctly exercises P1 (set-not-multiset on ℓ₃), P2 (ℓ₁/ℓ₂ identity), E4, the K.μ⁻ drop (Δ = −2 with k = 3), and the K.μ~ positional reordering (3 → 0). The D2 reordering formula now reads `Σ.M(d_q)(u)` (single inverse), consistent with the example.

The findings below are all anti-bloat / meta-prose, per the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Self-referential framing duplicates R0's content
**ASN-0107, "How the Count Changes: Links Retracted" intro**: "To withdraw a link from the count, in this model, is to remove it from the view, never from the store. We state this once, as the fact the withdrawal laws below all rest on."
**Problem**: The clause "We state this once, as the fact the withdrawal laws below all rest on" is meta-prose about R0's role, not content. The substantive half then duplicates R0's own closing line ("every 'withdrawal' removes a link from the view, never from the store"). The intro promises to state the fact once and R0 immediately restates it — two paragraphs saying the same thing.
**Required**: Drop the framing sentence and let R0 carry the claim, or fold the intro directly into R0.

### Issue 2: Forward-reference preview in "Two Anchorings"
**ASN-0107, "Two Anchorings, and the Tense of the Count"**: "Two anchorings present themselves, and E2 and D2 below establish that they differ precisely in monotonicity."
**Problem**: The clause previews downstream claims (E2, D2) rather than advancing the section's reasoning. The monotonicity distinction is established at E2 and D2 where it belongs; the forward pointer is pure signposting.
**Required**: Introduce the two anchorings without the downstream pointer.

### Issue 3: R3 parenthetical defers a case the claim already excludes and Open Questions already owns
**ASN-0107, R3 (PartialSurvival)**: "(the multi-arrangement reading, where the three parts are anchored to different documents, is deferred to the Open Questions)"
**Problem**: R3's setup already fixes a single resolved part `Qᵢ(Σ)`, so the multi-arrangement case is outside the claim's carrier; the parenthetical imagines and then defers an excluded case. Open Questions Q1 already owns exactly this topic, so the deferral is redundant with it. The same pattern recurs in R2's "(The multi-slot count change ... is not characterised here.)".
**Required**: Remove the in-claim deferral parentheticals; the Open Questions section is the correct and sufficient home for the multi-arrangement and multi-slot extensions.

## OUT_OF_SCOPE

The three Open Questions (independently-anchored parts, discovery/existence coincidence, count-vs-retrieval divergence) are correctly scoped as future work, not gaps in this ASN.

VERDICT: REVISE
