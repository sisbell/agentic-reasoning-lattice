# Revision Categorization — ASN-0058 review-3

**Date:** 2026-03-20 15:34

## Issue 1: Ordinal decrement via TumblerSub is broken for multi-component tumblers
Category: INTERNAL
Reason: The fix requires choosing a correct mathematical formulation for the predecessor operation. Both options (direct `pred` definition or subtraction-free reformulation) use only TumblerAdd and properties already established in ASN-0034. No design intent or implementation evidence is needed.

## Issue 2: M-aux domain omits k = 0
Category: INTERNAL
Reason: The fix is stating `v + 0 = v` as an explicit notational convention and restricting the TA-assoc derivation to positive arguments. All necessary definitions are already present in the ASN.

## Issue 3: M0 injectivity argument cites TA5(a) without establishing equivalence
Category: INTERNAL
Reason: The review itself provides the direct derivation path: TumblerAdd gives component form, T3 (CanonicalRepresentation) gives distinctness, T1 gives strict ordering. All cited properties are already established in ASN-0034.

## Issue 4: M16 cites T10 but T10 does not apply when origins are prefix-comparable
Category: INTERNAL
Reason: The review provides the correct argument: `origin(a₁ + n₁) = origin(a₁) ≠ origin(a₂)` implies `a₁ + n₁ ≠ a₂` by contrapositive. This uses only the origin function and ordinal increment properties already established in ASN-0034 and ASN-0036.
