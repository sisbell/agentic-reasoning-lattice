# Review of ASN-0098

This ASN is mathematically strong: all eight K-operations are covered (K.α/LP6, K.λ/LP7, K.ρ/LP14, K.δ node/account via the template and document/LP8, K.μ⁺ and K.μ⁺_L/LP9, K.μ⁻/LP10, K.μ~/LP11); boundary cases (empty endset, empty arrangement, full clearance `R=∅`, `n'_S=0`) are handled explicitly; the wp analysis (LP12a) is genuinely non-trivial; and both a worked trace and a worked numerical example are present. The LP-Fin interval-finitude proof is exhaustive in its case split. I found no correctness gap, no missing operation, no cross-ASN violation (all citations are to foundations 0034/0036/0043/0047/0093), and no implementation drift.

The findings below are prose-accretion issues surfaced under the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Self-restating bullets + roadmap in the projection definition
**ASN-0098, "The Projection Operation"**: "The definition reads from two inputs: — The endset, fixed once and for all... — The arrangement Σ.M(d), mutable... Of these two inputs, `coverage(e)` is endset-fixed (immune to transitions, by L12) and only `Σ.M(d)` varies; we therefore characterise projection displacement by examining what each editing operation does to `Σ.M(d)`."
**Problem**: The sentence after the bullets restates the two bullets verbatim (endset fixed by L12, arrangement varies) and then appends a roadmap ("we therefore characterise... by examining what each editing operation does"). This is the "two paragraphs say the same thing" pattern plus a forward roadmap that the section structure already conveys.
**Required**: Drop the restating sentence; the bullets already carry it. If the L12-immunity point is wanted near the definition, fold it into the first bullet and delete the roadmap clause.

### Issue 2: LP19 informally pre-states its own formal hypothesis
**ASN-0098, LP19**: "K.μ⁺ may add multiple V-positions `dom(Σ_{n+1}.M(d)) ∖ dom(Σ_n.M(d))` in a single step, each carrying its own I-address image; LP19's hypothesis selects, per V-position, only those whose image was freshly K.α/K.λ-allocated on the prefix. Formally, for every `v_new ∈ ...`"
**Problem**: The informal sentence is immediately re-expressed by the formal universal-over-`v_new` statement that follows. "May add multiple V-positions, each carrying its own image" is exactly what the formal per-`v_new` quantifier says; the reader must read the claim twice.
**Required**: Delete the informal pre-statement and keep the formal hypothesis, or keep one sentence of motivation but not a paraphrase of the formal text.

### Issue 3: Redundant gloss on the anchor exclusion
**ASN-0098, F definition**: "the sub-allocator anchors `b_C(d)` ... and `b_L(d)` ... have `#E = 1` and so lie outside `F`; they are anchors of chains, not chain elements."
**Problem**: "they are anchors of chains, not chain elements" restates "lie outside F" — the `#E = 1` fact already establishes exclusion (F-members have `#E = 2`). The trailing clause adds no inference.
**Required**: End the sentence at "lie outside `F`."

## OUT_OF_SCOPE

The Open Questions (reverse-discovery, V-order reflection, link-to-link induced discovery, cross-document "same operation sequence," fork non-transclusion, link-canonical contraction) are correctly deferred and not flagged.

VERDICT: REVISE
