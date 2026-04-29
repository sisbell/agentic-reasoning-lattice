# Revision Categorization — ASN-0065 review-1

**Date:** 2026-03-21 20:36

## Issue 1: Empty μ claim contradicts strict ordering requirement
Category: INTERNAL
Reason: The contradiction is between CS2 (strict ordering) and the paragraph's assumption c₁ = c₂, both stated within the ASN. The fix (delete or rephrase) requires only the ASN's own definitions.

## Issue 2: Non-foundation cross-ASN reference
Category: INTERNAL
Reason: The inline definitions of ord(v) and vpos(S, o) are already present in the ASN. The fix is purely editorial — remove the ASN-0061 attributions and let the self-contained definitions stand.

## Issue 3: No concrete worked example
Category: INTERNAL
Reason: All definitions needed to construct a numerical example (V-positions, I-addresses, cut sequences, postcondition clauses) are present in the ASN. The worked example is derived by instantiating the existing abstract definitions with specific tumbler values.

## Issue 4: R-SPERM proof omits case verification
Category: INTERNAL
Reason: The four postcondition clauses (R-S1, R-S2, R-S3, R-EXT) and the four permutation branches are all defined in the ASN. Each case verification is a mechanical substitution of one branch into the corresponding clause.
