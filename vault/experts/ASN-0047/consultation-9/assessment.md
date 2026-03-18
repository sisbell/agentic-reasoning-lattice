# Revision Categorization — ASN-0047 review-9

**Date:** 2026-03-17 05:01



## Issue 1: Temporal decomposition claim is ambiguous between elementary and composite transitions
Category: INTERNAL
Reason: The fix is a wording clarification — inserting "elementary" before "transition" — derivable entirely from the ASN's own definitions and coupling constraints.

## Issue 2: K.μ⁻ arrangement invariant preservation is asserted but not shown
Category: INTERNAL
Reason: The preservation argument (subset of a valid partial function is valid) follows from the definitions of S2, S3, S8a, S8-depth, S8-fin already present in the ASN. No external evidence needed.

## Issue 3: K.δ spans two layers but the temporal decomposition table classifies it as purely existential
Category: INTERNAL
Reason: The K.δ definition already states M'(e) = ∅ for documents; the fix is reconciling the summary table with the ASN's own content. No design-intent or implementation question arises.
