# Revision Categorization — ASN-0001 review-11

**Date:** 2026-03-01 19:27

## Issue 1: Definition of sig(t) contradicts its own example
Category: INTERNAL
Reason: The fix is a self-contained correction to a mathematical definition and its illustration — all needed information (the definition, the example, the intended semantics) is already present in the ASN.

## Issue 2: TA4 verification assumes aₖ > 0 without covering aₖ = 0
Category: INTERNAL
Reason: The missing sub-case (aₖ = 0) can be filled entirely from the constructive definitions of ⊕ and ⊖ already stated in the ASN — the review itself sketches the correct argument through the equal-operand path.

## Issue 3: TA3 proof does not cover the prefix case of a < b
Category: INTERNAL
Reason: The missing case follows from T1's prefix rule and the subtraction algorithm's zero-padding behavior, both already defined in the ASN — no external design intent or implementation evidence is needed.
