# Revision Categorization — ASN-0060 review-1

**Date:** 2026-03-21 01:55

## Issue 1: Free variable n in I6 and I7
Category: INTERNAL
Reason: The fix is purely notational — n ≥ 1 is already stated in the OrdinalShift definition and just needs to be pulled into the quantifier, following the pattern established by TA1 in ASN-0034.

## Issue 2: TA0 precondition not verified in OrdinalShift definition
Category: INTERNAL
Reason: The precondition m ≤ m is trivially satisfied from the definitions already in the ASN. The fix is adding one sentence stating TA0 holds, following ASN-0034's own discipline.

## Issue 3: No concrete example
Category: INTERNAL
Reason: The review itself supplies a correct worked example. The fix is mechanical — substitute specific values into the definitions already present in the ASN and verify.

## Issue 4: Shift composition not derived
Category: INTERNAL
Reason: The derivation uses only TA-assoc and TumblerAdd from ASN-0034, both already cited. The displacement addition δ(n₁, m) ⊕ δ(n₂, m) = δ(n₁ + n₂, m) follows directly from the TumblerAdd definition. No design intent or implementation evidence needed.

## Issue 5: Component positivity justification incomplete
Category: INTERNAL
Reason: Both cases (vₘ ≥ 1 and vₘ = 0) are resolved by n ≥ 1, which is already stated in the ASN. The fix is strengthening the justification to cover both cases using facts already present.
