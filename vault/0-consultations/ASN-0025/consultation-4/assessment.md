# Revision Categorization — ASN-0025 review-4

**Date:** 2026-03-07 08:18

## Issue 1: INSERT freshness derivation cites T9 alone
Category: INTERNAL
Reason: The ASN already cites T9, T10, and GlobalUniqueness in the P7 derivation. The fix is to replicate that same citation chain wherever freshness is asserted — all the needed properties are already present in the ASN.

## Issue 2: V-space postconditions for INSERT and DELETE are informal
Category: INTERNAL
Reason: The informal prose descriptions are already in the ASN and the formal notation style is established (J0, P0–P5). The fix is to restate existing prose claims as quantified postconditions using the same notation — no external evidence needed.

## Issue 3: {next} insertion position undefined
Category: INTERNAL
Reason: The concept is unambiguous from context (one past the maximum V-position, or the first position for an empty document). Defining it formally requires only the V-space model already in the ASN.

## Issue 4: Σ.D evolution not formalized
Category: INTERNAL
Reason: The review itself notes the ASN "has the pieces — P0, the orgl allocation in CREATE DOCUMENT and CREATE VERSION — but does not assemble them." The derivation is internal: if orgl(d) ∈ Σ.A and P0 prevents removal from Σ.A, then d cannot leave Σ.D. No external consultation required.
