# Revision Categorization — ASN-0040 review-11

**Date:** 2026-04-09 12:10



## Issue 1: B6 necessity proof omits the leading-zero sub-case
Category: INTERNAL
Reason: The fix is a proof restructuring — all T4 violation cases and their propagation via TA5(b) are already defined in the ASN. No external evidence needed.

## Issue 2: B1 proof asserts stream identity without derivation
Category: INTERNAL
Reason: The stream identity follows from TA5(d), TA5(c), and component comparison already present in the ASN. The derivation is mechanical algebra on definitions already stated.

## Issue 3: Foundation property cited by non-canonical name
Category: INTERNAL
Reason: The canonical name TA5a (IncrementPreservesT4) exists in ASN-0034. This is a cross-reference correction requiring no external evidence.

## Issue 4: B₀ non-emptiness split across two locations
Category: INTERNAL
Reason: Both the Σ.B definition and B₀ conf. are within this ASN. The fix is consolidating the non-emptiness requirement into B₀ conf. or adding an explicit note — no design intent or implementation evidence needed.
