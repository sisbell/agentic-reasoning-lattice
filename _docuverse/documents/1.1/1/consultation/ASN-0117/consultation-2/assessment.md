# Channel Assignment — ASN-0117 review-2

**Date:** 2026-06-08 17:23

## Issue 1: DEL-REMOVE / P1 makes a false domain claim and the worked example contradicts itself
Reason: Purely a logical correction internal to the ASN — restating removal in terms of V→I correspondences and the top-`c` labels that actually leave the domain. The corrected statement follows directly from DEL-DOM and DEL-SHIFT already present.

## Issue 2: LP10 (ContractionMonotonicity) is misapplied to DELETE
Reason: Internal fix — drop the LP10 citation and derive `ran(M'(d)) ⊆ ran(M(d))` directly from DEL-LEFT/DEL-SHIFT, exactly as the wp section already does. No external evidence or design intent is needed to remove a mis-cited lemma.

## Issue 3: ASN-0082 contraction lemmas are cited at S = s_C without establishing s_C = 1
Reason: Internal fix — the licensing fact `s_C = 1` is the foundation SubspaceConventionAxiom (ASN-0047/ASN-0093), so the repair is a citation already available in the foundation, requiring no design-intent or implementation input.
