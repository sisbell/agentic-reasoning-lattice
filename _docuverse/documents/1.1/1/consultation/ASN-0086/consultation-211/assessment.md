# Channel Assignment — ASN-0086 review-211

**Date:** 2026-06-01 16:38

## Issue 1: Non-load-bearing proof embedded in an Open Question
Reason: Editorial reduction — delete an embedded soundness derivation from a structural slot and restate the design tradeoff. Fully internal: the tradeoff is already named in the bullet and the derivation cites only ASN-0034 TA5 clauses already present.

## Issue 2: Home-prefix formula mis-attributed to L1a
Reason: A citation correction — point the NUDE-prefix projection formula at ASN-0043's `Home` definition and reserve L1a for the membership invariant. Both clauses are in the cited foundation; no design intent or implementation evidence is needed to pick the right one.

## Issue 3: "Value-shape postcondition (downstream hook)" — role-labeling and an auto-discharged "requirement"
Reason: Anti-bloat reframing — drop the role-label and restate L3-conformance as an auto-satisfied consequence of the typed signature, letting R5 verify its own triple. Derivable from R0's own quantification (`F, G ∈ Endset`, `K ∈ T_admissible`); internal.
