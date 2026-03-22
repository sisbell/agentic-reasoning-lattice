# Revision Categorization — ASN-0063 review-17

**Date:** 2026-03-22 00:15



## Issue 1: K.μ⁻ amendment not formalized
Category: INTERNAL
Reason: The fix requires formalizing a postcondition amendment for K.μ⁻ that parallels the existing K.μ⁺ amendment — all necessary definitions (D-CTG, D-MIN, D-SEQ) are already present in the ASN, and the constraint follows directly from them.

## Issue 2: K.μ~ D-CTG/D-MIN argument is circular
Category: INTERNAL
Reason: The fix replaces a circular derivation with the correct reasoning chain through K.μ~'s decomposition into K.μ⁻ + K.μ⁺, both of which have D-CTG/D-MIN postconditions already established (Issue 1 for K.μ⁻, existing amendment for K.μ⁺). All required definitions and properties are internal to the ASN.

## Issue 3: S3★-aux missing from ExtendedReachableStateInvariants
Category: INTERNAL
Reason: S3★-aux is already proved within the ASN and listed in the Properties table — the fix is purely editorial, either adding it to the conjunction or strengthening S3★ to subsume it. No external design intent or implementation evidence is needed.
