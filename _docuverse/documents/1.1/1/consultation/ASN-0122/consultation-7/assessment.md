# Channel Assignment — ASN-0122 review-7

**Date:** 2026-06-13 08:46

## Issue 1: X7(iii) asserts "X-T applies verbatim" but never discharges X-T's injectivity premise for the piecewise transport map
Reason: Internal. The fix discharges X-T's injectivity premise by invoking two ASN-0082 lemmas the reviewer has already named and stated — D-BJ (σ|R injective) and D-DP(a) (image-disjointness `L ∩ Q₃ = ∅`) — from a sibling spec the ASN already cites for this very case (D-SHIFT, D-L); no design intent or implementation evidence is involved, only a cross-reference within the spec corpus.

## Issue 2: X4c attributes content-instance-hood to consistency, when it follows from confinement
Reason: Internal. The region definition's `∩ V_{s_C}` clip already establishes that `P, Q` are content-confined; the fix simply swaps the cited premise from consistency to confinement, both of which are defined in the ASN.

## Issue 3: The "hygiene, not guarantee" point and its X9 losslessness deferral are duplicated between the region definition and the X12 precondition
Reason: Internal. Pure editorial deduplication — state the precondition plainly and keep the single clip/losslessness explanation in the region section; all content is already present in the ASN.

## Issue 4: Forward-pointer and significance-restatement accretion
Reason: Internal. Pure prose trimming of pre-statement pointers and interpretive restatements of already-proven claims; the underlying results (X2, the Windows and Self-Comparison X-claims) stay intact, so no channel input is needed to cut their restatements.
