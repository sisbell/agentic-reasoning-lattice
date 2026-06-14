# Channel Assignment — ASN-0134 review-43

**Date:** 2026-06-14 13:30

## Issue 1: Reviser-drift and defensive meta-prose around K.σ
Reason: Internal — the fix collapses to one derivation using inputs already present: ASN-0047's account-tier `A_doc` allocation (a cited dependency) and the Gregory "one query-and-increment path" evidence already cited in §4. The forced-vs-contingent collision distinction the reviser wants stated is derivable from material already in the note (the deterministic content/link H2 collision vs. the `d ∉ dom(M)` freshness-by-test it already articulates). No new design intent or implementation evidence is required.

## Issue 2: "global, not per-home" restated ~5× in the V2 region
Reason: Internal — pure deduplication of a conclusion the note already establishes; the supporting Q-affecting/constituent-kind argument is retained unchanged. No external channel bears on cutting redundant restatements.

## Issue 3: Meta-framing clause introducing the subspace-fusion caveat
Reason: Internal — deletes a justification sentence and re-leads an existing paragraph; the substantive caveat (abstract disjoint `s_C`/`s_L` frontiers vs. Gregory's fused granfilade) and its Gregory citation are already in the note and stay as written.

## Issue 4: §9 wp postcondition bundles model-intrinsic gaplessness into the serialization wp
Reason: Internal — reconciles the §9 wp with §5's W3, both already in the note; narrowing `R` to "fresh and unique" follows directly from W3's own claim that contiguity is model-intrinsic and serialization buys only same-home uniqueness. Purely an internal-consistency edit.
