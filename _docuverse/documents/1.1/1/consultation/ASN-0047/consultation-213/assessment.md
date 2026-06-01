# Channel Assignment — ASN-0047 review-213

**Date:** 2026-06-01 04:50

## Issue 1: K.μ~ S3★ verification mislabels a precondition-carried invariant as "discharged by the decomposition"
Reason: The fix is purely about internal labeling consistency between the matrix cell and Steps A/B — relabeling S3★(Σ') as precondition-carried by admissibility (i) versus realizability/non-vacuity. The logical dependency structure is fully present in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Document-level cross-document disjointness is re-proved from scratch despite being a foundation lemma, then double-discharged
Reason: The ASN already asserts that ASN-0093 supplies CrossDocumentDisjointness; collapsing the double-discharge and isolating the genuinely-new account-level/cross-subspace deltas is a restructuring derivable from the ASN's own citations and proof content.

## Issue 3: Forward-reference accretion / meta-prose (anti-bloat classifier)
Reason: Prose cleanup — deleting redundant forward pointers and relocating object content to its single definitional slot — is entirely internal and derivable from the ASN's existing structure.

## Issue 4: NodeLineage dropped from the end-of-document ExtendedReachableStateInvariants enumeration
Reason: Restoring NodeLineage to the summary enumeration is a token-level consistency fix against the authoritative invariant box already present in the ASN; no external input needed.
