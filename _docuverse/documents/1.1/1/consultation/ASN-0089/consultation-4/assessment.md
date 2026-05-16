# Revision Categorization — ASN-0059 review-4

**Date:** 2026-03-20 22:30

## Issue 1: Composite transition step (ii) is not well-defined when the shift is vacuous
Category: INTERNAL
Reason: The fix is purely structural — making step (ii) conditional and verifying coupling constraints for the reduced composite. All needed definitions (K.μ~, J0, J1, J1') are in ASN-0047, and the postcondition (I1–I5) is already correct for the vacuous case.

## Issue 2: Elementary preconditions at intermediate states not verified
Category: INTERNAL
Reason: The missing derivations use only properties already present in the ASN: I0(ii) with TA-strict for K.α freshness at intermediate states, and the shift displacement for K.μ⁺ domain availability. The review itself sketches the one-line arguments needed.
