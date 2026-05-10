# Revision Categorization — ASN-0064 review-5

**Date:** 2026-03-21 19:56

## Issue 1: F1 uses "partitions" but the per-block I-contributions may overlap or merge
Category: INTERNAL
Reason: The fix is purely notational — replacing "partitions" with "union" and noting count reduction. All definitions (canonical block decomposition M14, self-transclusion, I-adjacency) are already present in ASN-0058 and ASN-0064 itself.

## Issue 2: Variable ℓ used for both link addresses and span widths
Category: INTERNAL
Reason: This is a notation collision fixable by renaming variables. ASN-0043 already establishes the convention of using `a` for link addresses, and the span-width convention `ℓ` is standard across foundation ASNs — the fix just requires consistent application of existing conventions.
