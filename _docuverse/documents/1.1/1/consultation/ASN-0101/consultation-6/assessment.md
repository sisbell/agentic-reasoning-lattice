# Channel Assignment — ASN-0101 review-6

**Date:** 2026-05-27 15:37

## Issue 1: Containment precondition reduction skips the lex-order argument
Reason: The required derivation uses T1 trichotomy and S8a — both already cited foundations in the ASN. Fix is a one-paragraph expansion derivable from existing definitions.

## Issue 2: "K.μ~ exclusively over the content subspace" overreaches
Reason: Fix is a phrasing correction grounded in ASN-0047's existing definition of K.μ~. The substantive argument is preserved; only the scope-description needs rewording. No external evidence needed.

## Issue 3: Undefined notation `|dom_S(M(d))|`
Reason: Pure notational fix — either define `dom_S(M(d)) := V_S(d)` locally or rewrite using the existing `|V_S(d)|` form already used elsewhere in the ASN. Internal.

## Issue 4: Boundary cases assert D8 holds without case-by-case verification
Reason: The verification uses D0, D1, D8, and the foundation invariants already cited in ASN-0101. Tracing how each invariant clause degrades or receives a witness is internal proof-work, not a question of design intent or implementation behavior.
