# Revision Categorization — ASN-0047 review-3

**Date:** 2026-03-17 02:45

## Issue 1: Coupling constraints J0, J1, J1' are undefined for freshly created documents
Category: INTERNAL
Reason: The fix is a formal quantifier adjustment — either adopting the convention M(d) = ∅ for d ∈ E'_doc \ E_doc or quantifying over E'_doc. The ASN's own prose already describes the intended behavior ("some arrangement" without restriction), and J4 demonstrates the pattern for fork. The gap is between the formal statements and the already-stated intent.

## Issue 2: Foundation arrangement invariants not stated as transition constraints
Category: INTERNAL
Reason: The ASN already references ASN-0036 invariants selectively (S3 for K.μ⁺, S7a/S7b for K.α). The omission of S8a and S8-depth is a gap in the same pattern. The fix — requiring all ASN-0036 arrangement invariants to hold at composite transition boundaries — is derivable from the existing cross-references.

## Issue 3: Missing cross-layer invariants
Category: INTERNAL
Reason: Both invariants are one-step derivations from definitions already in the ASN. Existential coherence follows from K.α's S7a reference + J0's placement requirement. Provenance grounding follows from K.ρ's precondition (a ∈ dom(C)) + P0's monotonicity. The review itself notes the derivation is "straightforward."

## Issue 4: No concrete worked example
Category: INTERNAL
Reason: The ASN defines the address structure (via ASN-0034/ASN-0045 references), arrangement semantics (via ASN-0036), and all six elementary transitions with full postconditions. A worked example using concrete tumblers is constructible entirely from these existing definitions — no external design intent or implementation evidence is needed.
