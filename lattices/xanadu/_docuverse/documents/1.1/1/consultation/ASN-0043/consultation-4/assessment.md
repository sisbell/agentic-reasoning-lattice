# Revision Categorization — ASN-0043 review-4

**Date:** 2026-03-16 22:28

## Issue 1: L13 coverage characterization is weaker than what holds
Category: INTERNAL
Reason: The fix is a purely mathematical tightening — replacing "includes" with "equals" and adding a case analysis over tumbler depth. All required properties (T1, T4, TA5(c)) are already established in ASN-0034 and referenced in this ASN.

## Issue 2: Worked example omits L13 verification
Category: INTERNAL
Reason: The construction of a second link whose endset targets the first link uses only definitions already present in this ASN (L13, L4, L0, T12). The review specifies exactly what to build; no external design intent or implementation evidence is needed.

## Issue 3: Worked example asserts transition-dependent properties without justification
Category: INTERNAL
Reason: The fix is either constructing a concrete state transition within the example (e.g., adding a link and verifying L12 across the before/after states) or noting the vacuous satisfaction. Both options are derivable from the ASN's own definitions of L12 and L12a.

## Issue 4: Property table omits type classification
Category: INTERNAL
Reason: The INV/LEMMA/META classification follows from each property's logical role, which is determinable from the ASN's own content. The review already provides a suggested classification consistent with the foundation ASN convention (ASN-0034, ASN-0036).
