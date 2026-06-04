# Review of ASN-0091

## REVISE

### Issue 1: The S2/S5 "sharing is permitted" explanation is repeated three times
**ASN-0091, Net-effect split / Worked Example — Net-Effect Collapse / Worked Example — Bijection Non-Uniqueness**:
- Net-effect split: "Such an arrangement is permitted because S2 (ArrangementFunctionality) imposes *only* functionality on `M(d)`... and never a single-image (injectivity) constraint, so the same I-address may sit at several V-positions..."
- Collapse example: "The shared image is permitted because S2 (ArrangementFunctionality) imposes only functionality — each of `[1,1], [1,2], [1,3]` appears once on the left of the map — and never single-image injectivity..."
- Bijection example: "Sharing is permitted by S5 (UnrestrictedSharing)... this is admitted by S5 (UnrestrictedSharing) while S2 (functionality) still holds..."

**Problem**: The same foundational point — that functionality permits a shared image while forbidding multiple images per position — is restated in full three times. Two paragraphs in different sections saying the same thing in different words is the anti-bloat pattern.
**Required**: State the S2/S5 sharing licence once (the net-effect split is the natural site), and let the two worked examples cite it without re-deriving.

### Issue 2: The run-cardinality summary is stated twice in the same section
**ASN-0091, Run Decomposition Is Not Invariant**: After the RE-frag/RE-coal/RE-eq blockquotes — "Together, RE-frag, RE-coal, and RE-eq record that the maximal-run-decomposition cardinality is *neither monotonically non-decreasing nor monotonically non-increasing nor invariant*..." — and again as the section's closing sentence — "Run-decomposition cardinality is neither monotone nor invariant under rearrangement — it tracks the *visible structure*..."

**Problem**: Two sentences in one section carry the same conclusion. The closing sentence adds only the gloss "it tracks the visible structure," which can attach to the first occurrence.
**Required**: Delete one; fold any surviving gloss into the retained sentence.

### Issue 3: Preview sentences restate the derivation conclusion before deriving it
**ASN-0091, Subspace Frame / In-Subspace Exterior Frame**: Each section opens with "REARRANGE_K's cut-sequence structure delivers strict pointwise fixity..." and then the following paragraph derives exactly that from R-PPERM/R-SPERM + R-FRAME/R-EXT.

**Problem**: The preview sentence asserts the conclusion the next paragraph proves — redundant scaffolding. (The Subspace Frame's "not merely kept within their subspace" contrast with K.μ~ clause (iv) is genuine content and should be kept; the bare restatement of the conclusion is what is redundant.)
**Required**: Drop the conclusion-restating preview; retain the RE-sub/RE-ext orientation contrast if it carries the clause-(iv) distinction.

### Issue 4: `V_S(d) ≠ ∅` derived indirectly when R-PRE states it directly
**ASN-0091, REARRANGE as Vstream-Only Operation**: "REARRANGE_K excludes it via R-PRE(iv)... together with CS2's strict cut ordering, so `V_S(d) ≠ ∅` is a precondition of every REARRANGE_K invocation."
**Problem**: ASN-0084's R-PRE(ii) states `V_S(d) ≠ ∅` outright as a precondition. Routing the same fact through R-PRE(iv) + CS2 is a circuitous justification of something already given directly.
**Required**: Cite R-PRE(ii) directly.

## OUT_OF_SCOPE

### Topic 1: Reconstitution of a span split across non-contiguous fragments
**Why out of scope**: The ASN explicitly defers this (RE-trans note: "Whether the two fragments *jointly reconstitute* the original source span... is not established here") and lists it as an Open Question. It is new territory for a future ASN, not a defect here.

VERDICT: REVISE
