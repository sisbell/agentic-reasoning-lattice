# Channel Assignment — ASN-0091 review-5

**Date:** 2026-05-26 15:02

## Issue 1: RE-trans★ multi-step argument is misdirected
Reason: Pure logical fix using existing RE-ran and RE-other claims already established in the ASN. The corrected argument is fully derivable from the ASN's own content.

## Issue 2: 4-cut swap not concretely demonstrated
Reason: Constructing the trace requires R-SPERM's rewrite equations and R-DISP, both defined in ASN-0084 (already referenced in this ASN). All RE-* verifications are mechanical against existing claims in the ASN.

## Issue 3: RE-proj citation of RE-cov is incorrect
Reason: The fix is a citation correction grounded in the foundation's coverage definition (ASN-0098), already referenced in this ASN. No external channel needed.

## Issue 4: RE-frag direct witness conflates content-subspace and total cardinality
Reason: Pure clarification — make the empty-link-subspace property of the witness explicit, or modify the witness. Entirely internal cleanup.

## Issue 5: Abstract class admissibility not stated
Reason: This is a formal/architectural choice within the spec — whether to import K.μ~'s admissibility (ASN-0047) explicitly or require foundation-invariant preservation. The choice and its consequences for RE-sub's attribution are derivable from existing references; no design-intent question is at stake.

## Issue 6: Identity-exclusion claim about REARRANGE_K is over-strong
Reason: ASN-0084's R-PRE constraints (already referenced) force `w_α, w_β ≥ 1`, making π ≠ id automatic by construction. The corrected framing is derivable from the existing ASN-0084 reference.
