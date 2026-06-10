# Channel Assignment — ASN-0127 review-17

**Date:** 2026-06-10 03:55

## Issue 1: D-NONMONO's injective/non-injective split for K.μ~ is not the determinant it claims to be
Reason: This is a self-contained logical correction to a case analysis, not a question about design intent or implementation behavior. The determinant fix — split on ⊆-comparability of the moved image rather than injectivity, and add the incomparable-non-injective sub-case where F-IMONO is unavailable — is fully specified by the review and derivable from the ASN's own F-IMG-SWING cardinality fact (equal-size sets force incomparability; non-injectivity merely *permits* both containment and incomparable moves) plus the F-INERT/F-IMONO machinery already present. Neither Nelson's design intent nor Gregory's implementation evidence bears on whether the case split is logically exhaustive.
