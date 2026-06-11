# Channel Assignment — ASN-0117 review-35

**Date:** 2026-06-11 02:18

## Issue 1: Image notation declared, never used, and in conflict with restriction usage
Reason: Purely a notational cleanup internal to the ASN — the document's actual usage (`M(d)(Y)` for image, `|_` for restriction) is already established by its own formulas, so the fix is to delete or correct the stray convention sentence and audit occurrences. No design intent or implementation evidence bears on notation choice.

## Issue 2: Trace-validity chain derived twice in full
Reason: A structural deduplication of reasoning already present in the ASN — the validity chain is correct and merely stated twice, so the fix is choosing the single derivation site and replacing the duplicate with a citation. Neither channel is needed since no semantic content changes.
