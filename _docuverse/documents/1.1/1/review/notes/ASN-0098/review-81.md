# Review of ASN-0098

I checked every projection claim against its proof, verified operation coverage is complete (K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ — all eight transition kinds are accounted for, each as displacing or non-displacing), confirmed the boundary cases (empty endset, empty arrangement, R = ∅ contraction, orphan/resurrection), and worked through LP-Fin's interval-finitude argument case by case. The mathematics is sound: the prefix-agreement claim, the `#d ≤ #d_0` bound, sub-cases A/B, and the chain-index exhaustion all close. The wp derivations (LP12a, LP12b) and the worked trace check out.

The note has effectively converged on correctness. The one residual item is signposting prose, which the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: "Two further questions" intro miscounts and misframes the section
**ASN-0098, "Boundary and Width Behaviour"**: "We address two further questions about the structural behaviour of projection under specific operation patterns."
**Problem**: This is deletable roadmap prose that does not advance reasoning, and it is inaccurate. The section presents far more than two questions and several claims that are not about "operation patterns" at all: LP20 (RangeConfinement) and LP21 (RepresentationInvariance) are state-fixed structural facts independent of any operation, and LP12b is a wp evaluation. The reader who tries to map "two questions" onto the section's contents (LP-Sub, LP-Fin, LP-Fin Corollary, LP12b, the `tight` definition, LP19a, LP19, LP20, LP21) must abandon the count immediately. The intro sentence and the "Boundary and Width Behaviour" heading both mis-describe their contents — LP20/LP21 concern neither boundaries nor width.
**Required**: Delete the roadmap sentence (the section flows directly into the `F` definition without it), or rewrite it to name what the section actually establishes. If LP20/LP21 are to stay, either relocate them out from under a heading they do not belong to, or widen the heading to match.

## OUT_OF_SCOPE

No claims in the ASN encroach on the excluded topics (link type semantics, replication/BEBE). The Open Questions section correctly defers reverse-discovery, V-order reflection, link-to-link induced discovery, cross-document operation comparison, and link-canonical contraction to future ASNs rather than asserting them here. No OUT_OF_SCOPE flags required.

VERDICT: REVISE
