# Channel Assignment — ASN-0086 review-232

**Date:** 2026-06-01 20:03

## Issue 1: "Layer-reachable" domain is degenerate — no document is ever allocated, so Emit_K is never enabled
Reason: The fix is purely definitional — redefine "layer-reachable" as `→*`-reachable states permitting freely-interleaved K.σ/K.α steps with the unit-depth discipline on `L_R`-growing K.λ steps, then extend the induction Step to K.σ/K.α (trivial, since both leave `Σ.L` unchanged per their frame conditions already stated in the note). All needed pieces — the `→ ≡ K.σ ∪ K.α ∪ K.λ` definition and the frame conditions — are present in the ASN.

## Issue 2: `nullified(Σ)` computability does not discharge selection of `L_R^Σ`
Reason: The fix is to cite the note's own Lemma CoverageEqualityDecidable for the `L_R^Σ` slice-selection step, exactly as already done for `L_K^Σ`. The lemma is internal to the ASN; no external evidence or design intent is required.

## Issue 3: Anti-bloat — proof-structure narration and duplicated conformance prose
Reason: Purely editorial — delete the announcement sentence and consolidate the four redundant L3-conformance restatements into one referenced check. No design intent or implementation evidence bears on prose pruning.
