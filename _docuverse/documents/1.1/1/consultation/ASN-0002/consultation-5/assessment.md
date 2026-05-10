# Revision Categorization — ASN-0002 review-5

**Date:** 2026-03-06 14:30

## Issue 1: COPY's V-space effect is underspecified
Category: GREGORY
Reason: The ASN needs implementation evidence about how COPY modifies the target document's V-space — whether it shifts existing V-positions like INSERT, what determines the insertion point, and whether subspace isolation holds. Gregory's INSERT evidence (two-blade boundary, uniform shift) cannot be assumed to apply to COPY without confirmation.
Gregory question: When COPY inserts I-addresses into the target document's V-space, does it shift existing V-positions at or beyond the insertion point (like INSERT does), and is the shift confined to the same subspace as the copied content?

## Issue 2: DELETE subspace isolation asserted by "mirrors," not independently established
Category: INTERNAL
Reason: The ASN already contains Gregory's evidence (exponent guard making cross-subspace subtraction a no-op). The fix is restructuring: elevate this existing evidence into a labeled property parallel to AP6, rather than leaving it as a "mirrors" assertion in a frame-condition paragraph.

## Issue 3: AP14 verification relies on "analogous confinement"
Category: INTERNAL
Reason: Each operation takes a single document parameter and has no mechanism to access another document's V-space. The arguments are derivable from the operation signatures and effect descriptions already stated in the ASN — they just need to be written out explicitly instead of analogized.

## Issue 4: CREATELINK home/endpoint distinction is ambiguous
Category: INTERNAL
Reason: AP16 already establishes that CREATELINK writes only to the home document's link subspace and reads only from endpoint documents' text subspace. When home = endpoint, these are disjoint subspaces with no interference. The fix is removing the "distinct from" claim and adding one sentence confirming validity, grounded in AP16.
