# Review of ASN-0053

## REVISE

### Issue 1: Level-uniformity closure not stated as postcondition
**ASN-0053, S1/S3/S4/S8**: Each operation's proof establishes the lengths of all intermediate tumblers but never draws the explicit conclusion that the output span is level-uniform.
**Problem**: Composability depends on level-uniformity being preserved. If you split a span (S4) and then want to merge one part with another span (S3), you need the split output to be level-uniform — S3's precondition demands it. The reader must re-derive this from the length calculations already present in each proof. For S1: #s' = #r' is established, so γ = (s', r' ⊖ s') has #start = #width = #s'. For S3: #s = #r, so the merged span has #start = #width. For S4: #d = #s and #d' = #s, so both λ and ρ are level-uniform. For S8: each emitted span has #s = #r by level-compatibility of the input, so #start = #width. The facts are in the proofs; the conclusions are not.
**Required**: Add an explicit postcondition to S1, S3, S4, and S8 stating that the output span(s) are level-uniform when the inputs are level-uniform and level-compatible. One sentence per operation suffices — e.g., for S3: "The merged span γ is level-uniform: #start(γ) = #s = #(r ⊖ s) = #width(γ), since #s = #r by level-compatibility."

### Issue 2: S11 asserts representability without construction
**ASN-0053, S11**: "Each non-empty interval is a half-open interval on the tumbler line, representable as a span when α and β are level-uniform (ensuring D0 and D1 hold for the boundary tumblers)."
**Problem**: The proof identifies the two remainder intervals but never constructs the spans or verifies T12 for them. This is an assertion of representability, not a proof of it. For the left interval {t : start(α) ≤ t < start(β)}, the span is (start(α), start(β) ⊖ start(α)); for the right interval {t : reach(β) ≤ t < reach(α)}, it is (reach(β), reach(α) ⊖ reach(β)). Each needs: (1) the width is positive (divergence at some k with a positive component), (2) the action point k ≤ #start, (3) the reach round-trip holds via D1. These follow from level-uniformity and level-compatibility, but the steps are not shown.
**Required**: Explicitly construct both difference spans, verify T12 for each, and add a concrete example — e.g., α = ([1, 3], [0, 8]) containing β = ([1, 5], [0, 4]): left = ([1, 3], [0, 2]), right = ([1, 9], [0, 2]), verify reaches and denotations.

### Issue 3: Split-merge inverse claimed without derivation
**ASN-0053, S5 discussion**: "This composition property makes split and merge inverses: merge the two split parts, and the resulting width is d ⊕ d' = ℓ, recovering the original span exactly."
**Problem**: S5 establishes d ⊕ d' = ℓ (width composition), but the claim "recovering the original span exactly" requires more: that the merge of λ and ρ produces a span with start s and reach reach(σ). The merge (S3) constructs γ = (min(start(λ), start(ρ)), max(reach(λ), reach(ρ)) ⊖ min(start(λ), start(ρ))). Showing this equals σ requires: min(s, p) = s (since s < p), max(p, reach(σ)) = reach(σ) (since p < reach(σ)), and reach(σ) ⊖ s = ℓ (by the level-uniform reach round-trip). The path goes through S3's construction and D1, not through S5 directly. S5 gives an algebraic identity about widths; the split-merge inverse also needs the start and reach to line up.
**Required**: Either state and prove the split-merge inverse as a formal property (merge(λ, ρ) = σ), or expand the S5 discussion to show the full chain: merge start = s, merge reach = reach(σ), therefore merge width = reach(σ) ⊖ s = ℓ.

## OUT_OF_SCOPE

### Topic 1: Span-set intersection
S1 handles intersection of two spans. Intersection of two span-sets (producing a normalized span-set) is a natural extension that would require iterating S1 over pairs and normalizing the results.
**Why out of scope**: S1 provides the building block; the span-set extension is a compositional consequence that belongs with span-set operations in a future ASN.

### Topic 2: Cross-depth span operations
The level constraint S6 restricts all constructive operations to same-depth operands. The open questions correctly identify cross-depth split and intersection as unresolved.
**Why out of scope**: The ASN establishes the same-depth algebra completely; cross-depth behavior requires new definitions (depth coercion or projection) that are genuinely new territory.

VERDICT: REVISE
