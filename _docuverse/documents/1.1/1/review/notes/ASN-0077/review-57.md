# Review of ASN-0077

This note carries the `review-mode.anti-bloat` classifier. The mathematics is sound and has clearly survived many revision cycles — the singleton-span proof (O10 edge cases), the equivalence chain (F1)≡(F2)≡(F3), and the K.μ~ admissibility discharge in the worked example are all rigorous and complete. My findings are confined to forward-reference / redundancy accretion of the kind the classifier targets.

## REVISE

### Issue 1: Same fact restated four times across the transclusion section
**ASN-0077, "Direct resolution through transclusion"**: The pre-O4 paragraph and the post-O4 paragraph repeat the identical observation in different words:
- "the I-address recorded in every intermediate document's arrangement is the *same*"
- "records exactly the original I-address `a` rather than a copy"
- "the address does not change as it propagates"
- "Each intermediate document's arrangement independently records the same `a`"
- (post-O4) "Each intermediate `dᵢ` independently registered ... an entry mapping one of its V-positions to the I-address `a`"
- (post-O4) "The shared identity of `a` across all intermediate arrangements ..."
- (post-O4) "by O4, every intermediate document holds the same `a`"

**Problem**: This is the "two paragraphs say the same thing in different words" pattern. The single load-bearing fact (intermediate arrangements record the original `a`, so no chain is walked) is asserted ~7 times.
**Required**: State the fact once. O4's derivation already establishes interchangeability from the pure projection; collapse the surrounding prose to a single sentence.

### Issue 2: J4/K.μ⁺ scaffolding does not advance O4
**ASN-0077, "Direct resolution through transclusion"**: "The mechanism is foundation: K.μ⁺ (ArrangementExtension, ASN-0047) admits any allocated I-address ... and J4 (ForkComposite, ASN-0047) propagates I-address ranges through forks ... together they realize O4's hypothesis along any chain of transclusion operations."
**Problem**: O4's claim *assumes* the hypothesis ("suppose `d₂, …, dₙ` are distinct documents each holding a V-position with `M(dᵢ)(vᵢ) = a`") and its derivation never consults J4 or K.μ⁺. This paragraph explains *how the hypothesized state arises* rather than proving the claim — scaffolding around the claim, not reasoning within it.
**Required**: Remove the realizability digression, or compress to a one-clause pointer; it is not part of O4's proof.

### Issue 3: Defensive "not by S8-depth" clause
**ASN-0077, "Lifting origin to a V-span"**: "Mixed V-spans (crossing both subspaces) are excluded by the conjunction of C0 ... and C0a ... — *not by S8-depth, which permits distinct subspaces to share a common depth* (a link-subspace depth `m_L(d)` may coincide with a content-subspace depth `m_C(d)`, where a depth coincidence does not force subspace coincidence)."
**Problem**: The parenthetical justifies what does *not* establish the result. This is a defensive justification of the kind the anti-bloat guidance flags; the positive statement (C0 + C0a force single-subspace confinement) stands on its own.
**Required**: Drop the "not by S8-depth …" clause; keep the C0/C0a derivation.

### Issue 4: Tool-choice justification stated as prose
**ASN-0077, "Lifting origin to a V-span"**: "ASN-0058's `resolve` cannot serve here: its C1 (ResolutionIntegrity) asserts `aⱼ + i ∈ dom(C)`, whereas SHOWORIGIN_V admits link-subspace V-spans whose I-targets lie in `dom(L)`; C1a's decomposition covers both subspaces."
**Problem**: This is a "why I picked tool X over tool Y" note. The argument simply uses C1a; the rejected alternative adds no reasoning the reader needs to follow the construction.
**Required**: Remove or fold into a half-sentence at the point C1a is first invoked.

## OUT_OF_SCOPE

### Topic 1: Reporting link origins from an I-span
Correctly deferred to the ASN's own Open Question 1. The I-span lift intentionally intersects only `dom(C)`; surfacing link origins from an I-span is new territory, not an error here.

### Topic 2: Historical containment via Σ.R
The "What SHOWORIGIN does not promise" section correctly bounds the operation to current-arrangement origin and routes historical containment to a separate future operation. Appropriate exclusion.

VERDICT: REVISE
