# Channel Assignment — ASN-0116 review-50

**Date:** 2026-06-09 17:58

## Issue 1: `coverage` carries a state subscript that the foundation forbids
Reason: The fix is a mechanical notation substitution fully specified by the review, which already quotes the foundation form (ASN-0098's "purely combinatorial" statement and LP3★'s native `coverage(Σ.L(a).eᵢ)` with state inside the argument). Replacing the subscripted `coverage_{Σ}(e)` with the foundation form is derivable from the ASN's existing L12+LP3★ citation; no external channel is needed.

## Issue 2: the block-disjointness intervals are re-derived after being cited
Reason: Pure anti-bloat editorial fix — drop the redundant re-listing of the three intervals (already established verbatim in the Effect section's block-disjointness fact) and keep the genuinely new Q10 reading-order conclusion and starred→unstarred reduction. Entirely derivable from the ASN's own text.

## Issue 3: IP1's "within the S8★ partition" can mislead — the inserted block need not be a maximal-run element
Reason: The softening follows from the ASN's own allocator semantics (`a = inc(a_prev, 0)`, exactly one above the max origin-`d` content address) plus the S8/S8★ definitions the ASN already cites; backward I-adjacency arises whenever `a_prev` is arranged at `q_{J-1}` — the ordinary repeated-append configuration, already within the ASN's model where arrangement order need not equal content order (cf. the worked example's unarranged `a_max = [d.0.s_C.6]` over only five arranged positions). K.μ~ reorder is already cited in the ASN, so no new design intent or implementation evidence is required.
