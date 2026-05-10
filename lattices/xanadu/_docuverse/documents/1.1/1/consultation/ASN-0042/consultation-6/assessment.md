# Revision Categorization — ASN-0042 review-6

**Date:** 2026-03-15 21:54

## Issue 1: O9 claims node-field equality but proof yields only prefix containment
Category: INTERNAL
Reason: The fix (weaken to prefix containment or add a case split by zero count) is fully derivable from T4 field structure, T5 prefix relation, and O1a already present in the ASN. No design intent or implementation evidence is needed.

## Issue 2: `≺` (strict prefix) used without definition
Category: INTERNAL
Reason: The definition `p ≺ a ≡ p ≼ a ∧ p ≠ a` follows directly from the existing `≼` (T5) definition in ASN-0034. This is a missing one-line definition, not a conceptual gap.

## Issue 3: O8 proof cites O5 (allocation) for a delegation conclusion
Category: INTERNAL
Reason: The correct citation — condition (ii) of the `delegated` relation — is already defined in this ASN with the identical "most-specific covering principal" constraint. The fix is replacing a wrong cross-reference with the right one.
