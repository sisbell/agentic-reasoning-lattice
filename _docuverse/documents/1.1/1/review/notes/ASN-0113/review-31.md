# Review of ASN-0113

The technical core is sound. I checked the extent-span construction (W2/W3), the exact-coverage derivation (W4), the contiguity-necessity argument (W5), subspace confinement (W10/W11), and the worked instances (including the depth-3 case that exercises T5's prefix-confinement non-vacuously). The T5 application in W4, the TumblerAdd reach computations, the order-convexity argument in W5's converse, and the XOR formulation in W19 all hold. Foundation usage (D-SEQ★, S3★-aux, CL-OWN/CL-UNIQ, T12, S0) is correct and the ASN does not reinvent foundation notation.

The findings below are anti-bloat / prose items, consistent with this note's `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Structural meta-comment and intro restatement in W0
**ASN-0113, "What the caller must be handed"**: "Before specifying the operation we fix the *type* of its result; the intro carries the Nelson framing. The result is a *normalized span-set* `Σ_d` of at most two members ... never a content read ... and never a pair of bare integers."
**Problem**: The clause "the intro carries the Nelson framing" is a comment about document structure, not about the claim — exactly the meta-prose pattern flagged (prose about ordering/structure rather than content). The surrounding sentence also re-asserts the intro's already-stated "span-set, not a single span" point in new words ("never a content read," "never a pair of bare integers"), so the reader crosses the same ground twice.
**Required**: State W0's result type directly. Drop the structural aside; if the content/integer contrast is worth keeping, state it once and not as a paraphrase of the intro.

### Issue 2: W14 asserts only the trivial half and defers the substantive half
**ASN-0113, "Invariants across the members" (W14)**: "Comparability — for any two allocated documents `d₁, d₂`, the per-kind comparison `n_S(d₁)` versus `n_S(d₂)` is well-defined ... The comparison is total because `n_S(d) = |V_S(d)|` counts `V_S(d)` directly (W1)."
**Problem**: As stated, W14 reduces to "`n_S` is a total function," which is already W1. The genuinely substantive question it gestures at — how a consumer reads an *omitted* member when comparing reports across documents of differing vintages — is then punted to an Open Question. So the claim asserts the easy consequence and defers the hard content, while sitting in the "invariants across the members" section though it concerns comparison *across documents*, not across members of one report.
**Required**: Either fold the totality remark into W1's stated consequences (it adds nothing standalone), or give W14 substantive cross-member content. If kept, relocate it out of the across-members invariants slot.

## OUT_OF_SCOPE

(none — the note correctly confines version-fork, transclusion, and overall-extent-consistency to the Open Questions and introduces no claims for them.)

VERDICT: REVISE
