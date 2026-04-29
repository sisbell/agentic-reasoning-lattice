# Revision Categorization — ASN-0059 review-1

**Date:** 2026-03-20 21:30

## Issue 1: V-position depth ≥ 2 not required
Category: INTERNAL
Reason: The fix is derivable from existing definitions. A V-position must encode both subspace (position 1) and ordinal (position ≥ 2), so #p ≥ 2 follows from the subspace/ordinal structure already defined in the ASN. The review even sketches the derivation chain.

## Issue 2: Domain completeness attributed to I1–I4 but requires the composite
Category: INTERNAL
Reason: This is a proof-structure gap — I1–I4 give ⊇ but not ⊆. The fix is to add an explicit frame postcondition or reattribute the ⊆ direction to the composite transition analysis, both of which use material already present in the ASN.

## Issue 3: No concrete worked example
Category: INTERNAL
Reason: The reviewer sketches the exact scenario needed. Constructing the example is mechanical application of I0–I3 and I10 to concrete tumblers, requiring no external evidence.

## Issue 4: Block split offset derivation missing
Category: INTERNAL
Reason: The reviewer provides the full prefix-agreement argument. The derivation uses only the definition of ordinal increment (TA5(c) modifies position m only) and the straddling condition v < p < v + k — all internal to the ASN and its dependencies.

## Issue 5: shift-ordinal commutativity by handwave
Category: INTERNAL
Reason: The fix is to cite M-aux (OrdinalIncrementAssociativity, ASN-0058) and show the component-level verification. Both the citation and the verification are available from existing ASN content.

## Issue 6: Incorrect citation for IsElement precondition
Category: INTERNAL
Reason: The reviewer provides the correct derivation chain (I0(iii) → origin well-defined → zeros(aᵢ) = 3 → IsElement(aᵢ)) using definitions from ASN-0034 and ASN-0036. The fix is a citation correction using existing material.
