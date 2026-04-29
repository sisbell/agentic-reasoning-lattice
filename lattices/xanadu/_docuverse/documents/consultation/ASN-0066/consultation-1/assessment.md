# Revision Categorization — ASN-0066 review-1

**Date:** 2026-03-21 12:57

## Issue 1: Cross-references to non-foundation ASN-0047
Category: INTERNAL
Reason: The review already specifies how to restate everything self-containedly using ASN-0036 (empty initial state) and inline reasoning (single interior removal breaks contiguity). No external evidence needed.

## Issue 2: Undefined notation K.μ⁻
Category: INTERNAL
Reason: The review provides the exact restatement: "Removing a single interior V-position from dom(M(d)) violates D-CTG." This is a notation cleanup derivable from the ASN's own definitions.

## Issue 3: DELETE preservation claimed without proof
Category: INTERNAL
Reason: The simpler fix — uniformly deferring all operations including DELETE — requires no external evidence. Even proving preservation (contiguous range removal + shift-down yields contiguous result) is derivable from the definitions already present.

## Issue 4: Depth > 2 consequences not derived
Category: INTERNAL
Reason: The consequence (D-CTG + S8-fin + S8a forces shared intermediate components at depth ≥ 3) is a mathematical derivation from properties already stated in this ASN and ASN-0036. The review itself derives it.

## Issue 5: No concrete verification example
Category: INTERNAL
Reason: The review provides a ready-made example using the ASN's own definitions. Constructing a concrete state and checking D-CTG requires only the formal statement already present.

## Issue 6: Starting-position constraint absent
Category: NELSON
Reason: Nelson's quote specifies "addresses 1 through 100," implying positions start at 1. Whether this is a prescriptive design constraint or merely an illustrative example is a question about design intent that only the Nelson source can resolve.
Nelson question: Does the Vstream design require that V-positions within a subspace always start at ordinal 1 (i.e., addresses are 1 through n), or is the starting position determined by the allocation mechanism and intentionally left unspecified?
