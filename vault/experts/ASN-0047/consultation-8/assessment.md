# Revision Categorization — ASN-0047 review-8

**Date:** 2026-03-17 04:34



## Issue 1: K.μ⁺ uses C' and R' in two incompatible senses
Category: INTERNAL
Reason: This is a notational consistency problem entirely within the ASN's own definitions. The fix — disambiguating elementary vs. composite post-states — requires only reorganizing or annotating existing material.

## Issue 2: Worked example does not verify P8
Category: INTERNAL
Reason: P8 is defined in this ASN, the worked example's state is fully specified, and the verification (parent(d₂) = 1.0.1 ∈ E₁) follows directly from the given data. No external evidence needed.

## Issue 3: K.μ⁺ S8-depth precondition is stated per-position but the invariant is cross-position
Category: INTERNAL
Reason: S8-depth is already defined in ASN-0036/ASN-0047; the fix is rewording the precondition to reference the resulting arrangement rather than the new positions alone. No design-intent or implementation evidence is needed.
