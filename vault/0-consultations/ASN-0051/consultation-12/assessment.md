# Revision Categorization — ASN-0051 review-12

**Date:** 2026-03-23 00:43

## Issue 1: Worked example performs an invalid contraction
Category: INTERNAL
Reason: The fix (replace single interior K.μ⁻ with K.μ~ then K.μ⁻ from the end) is fully specified by K.μ⁻'s D-CTG/D-SEQ postconditions already defined in ASN-0047. The review even provides the valid composite.

## Issue 2: K.μ⁺_L and K.λ omitted from survivability analysis
Category: INTERNAL
Reason: Both operations are fully defined in ASN-0047 with explicit frame conditions. K.λ preserves M (add to frame list), K.μ⁺_L extends ran(M(d)) (same proof structure as SV2). All information needed is in the existing foundation ASNs.

## Issue 3: False claim about non-text V-positions
Category: INTERNAL
Reason: K.μ⁺_L is already defined in ASN-0047 as creating link-subspace V-positions. The correction is a direct consequence of that definition — replace the false equality claim with the subset relationship.

## Issue 4: Name collision with foundation definition of resolve
Category: INTERNAL
Reason: This is a naming conflict between two definitions both visible in the spec. The fix is a mechanical rename of the ASN-0051 function; no external evidence is needed to choose an unambiguous name.

## Issue 5: Fragment splitting mechanism incorrectly attributed to single contraction
Category: INTERNAL
Reason: K.μ⁻'s postcondition (removal from maximum end only) is already defined in ASN-0047. The correction — that splitting requires K.μ~ followed by K.μ⁻, not K.μ⁻ alone — follows directly from these existing definitions.
