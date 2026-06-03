# Channel Assignment — ASN-0070 review-76

**Date:** 2026-06-03 03:41

## Issue 1: F-det re-narrates F-canonical's internal proof instead of citing its result
Reason: Purely internal restructuring — F-canonical (within this ASN) already proves uniqueness-from-V-restricted-denotation, so collapsing step 4 to a citation and trimming the Depends list is derivable from the ASN's own content. No design intent or implementation evidence is needed.

## Issue 2: F-empty re-explains F-canonical's Step 0 / Step 3 rather than citing uniqueness
Reason: Internal proof-hygiene fix — F-canonical's uniqueness clause already covers the canonical form of ∅ for both vacuous and populated-but-empty subspaces, so replacing the re-derivation with a citation is derivable from the ASN alone. No external channel is required.
