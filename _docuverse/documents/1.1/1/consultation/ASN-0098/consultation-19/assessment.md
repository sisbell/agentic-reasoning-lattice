# Channel Assignment — ASN-0098 review-19

**Date:** 2026-05-26 03:17

## Issue 1: LP19's hypothesis ambiguous about per-pair scope under K.μ⁺ multi-mapping
Reason: Pure wording clarification — the lemma's mathematical content is sound, and K.μ⁺'s multi-mapping behaviour is already cited from ASN-0047 elsewhere in the ASN (LP9's effect-clause discussion). The fix restates the hypothesis to bind (v_new, a_new) per-pair, derivable from the existing ASN-0047 references.

## Issue 2: Empty endset projection statement lacks domain qualification
Reason: Pure formal precision — the `project` definition's precondition `d ∈ dom(Σ.M)` is already stated immediately above the degenerate-configuration sentences. The fix is a quantifier scope adjustment derivable from the ASN's own convention.

## Issue 3: Achievability subsection redundant with LP-Fin Corollary
Reason: Editorial/structural decision about exposition — the relationship between the four cross-document sub-cases and the corollary they instantiate is internal to the ASN. Either flagging redundancy or collapsing the cases requires only the ASN's own content.

## Issue 4: LP12a second boundary case forward-references LP-Fin Corollary
Reason: Organizational choice about placement of LP-Fin within the ASN's flow, or whether to introduce a tracked label (e.g., LP12b) for the deferred discharge. Decision derivable from the ASN's own structure without external input.
