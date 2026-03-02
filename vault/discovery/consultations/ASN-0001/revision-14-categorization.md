# Revision Categorization — ASN-0001 review-14

**Date:** 2026-03-01 20:15



## Issue 1: Span length representation claim contradicts constructive definition
Category: INTERNAL
Reason: The fix requires clarifying the relationship between the already-defined constructive addition (action point semantics) and the informal span length characterization. All necessary information — TA0's precondition, the constructive definition of ⊕, and the I-space address structure — is already present in the ASN.

## Issue 2: TA7a formal statement underdetermined on representation
Category: INTERNAL
Reason: The ASN's own verification section already resolves the ambiguity by adopting the ordinal-only formulation, and the worked example confirms it. The fix is to promote that resolution into the formal statement — no external evidence needed.

## Issue 3: Worked example does not verify T12 for I-space spans
Category: INTERNAL
Reason: All ingredients for the I-space span example are already present in the worked example (the five I-space addresses, the constructive definition of ⊕, and T12's definition). The fix is purely additive composition of existing content.
