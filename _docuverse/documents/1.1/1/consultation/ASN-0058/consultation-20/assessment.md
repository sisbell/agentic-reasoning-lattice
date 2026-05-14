# Channel Assignment — ASN-0058 review-20

**Date:** 2026-05-13 19:59

## Issue 1: "v + 0 = v" convention used before formal introduction
Reason: Pure presentation fix — the convention already exists in M-aux and just needs to be hoisted before M0. No design intent or implementation evidence required.

## Issue 2: Mapping blocks are subspace-confined, but the property is never stated
Reason: Structural property already derivable from OrdShiftHom + S8-depth (ASN-0036), repeatedly used in the ASN's own proofs. Elevating it to a labeled corollary is internal refactoring.

## Issue 3: Resolution V-ordering claim is informal commentary, ambiguously worded
Reason: Wording/labeling clarification of a property already implicit in the "ordered by V-start" phrase in the resolution definition. No external input needed.

## Issue 4: M16 relies on T4-validity of a₁ but never cites the source
Reason: Citation chain (a₁ ∈ dom(C) → S7a/S7d allocator → T10a.4 T4-validity) is fully present in ASN-0036 and ASN-0034 dependencies; the fix is to make the citation explicit at the top of M16's proof.
