# Channel Assignment — ASN-0115 review-8

**Date:** 2026-06-05 06:28

## Issue 1: Novel boundary claims asserted but never verified against a concrete scenario
Reason: The fix is internal — both worked instances instantiate claims (R10, R11) and substrate operations (K.μ⁻ contraction per ASN-0047 P3, the item tagging from R0) already defined and justified in the ASN, including its existing Nelson/Gregory citations. Constructing concrete examples from the established model requires no new design intent or implementation evidence.

## Issue 2: R11's weakest-precondition statement is non-minimal — condition (ii) is entailed by (i)
Reason: The fix is internal — S3★ (already cited in the ASN) gives `M(d)(v) = a ⟹ a ∈ dom(Σ.C)` for content positions, so the entailment of (ii) from (i) is derivable entirely from the ASN's own substrate claims with no external input.
