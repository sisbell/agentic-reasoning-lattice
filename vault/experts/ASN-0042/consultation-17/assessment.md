# Revision Categorization — ASN-0042 review-17

**Date:** 2026-03-16 07:39



## Issue 1: Missing state axiom — T4 validity of allocated addresses
Category: INTERNAL
Reason: The fix is adding an explicit axiom for a property already assumed throughout the ASN. The content needed — that allocation preserves T4 — is derivable from the existing framework (T4 is defined in ASN-0034, and the axiom's form mirrors O12–O16).

## Issue 2: O7(a) postcondition is tautological and state-ambiguous
Category: INTERNAL
Reason: The fix is tightening a formal statement and adding state subscripts. The correct postcondition and its justification follow directly from the delegation relation's conditions (i) and (vi) already defined in the ASN.

## Issue 3: Domain nesting characterization excludes same-level nesting
Category: INTERNAL
Reason: The general property `pfx(π₁) ≼ pfx(π₂) ⟹ dom(π₂) ⊆ dom(π₁)` follows from transitivity of the prefix relation, which is already established. The same-level nesting case is discussed later in the ASN itself — this is a presentation fix to align the formal statement with the ASN's own content.
