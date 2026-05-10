# Revision Categorization — ASN-0063 review-11

**Date:** 2026-03-21 21:38



## Issue 1: P4★ preservation argument omits K.μ~ (reordering)
Category: INTERNAL
Reason: The fix is explicitly identified in the review — connect the existing link-subspace fixity proof (already in the S3★ section) to the P4★ preservation argument. All necessary reasoning is present in the ASN.

## Issue 2: K.μ⁺ amendment impact on J4 (ForkComposite) not acknowledged
Category: NELSON
Reason: Whether a forked document should inherit its source's link-subspace mappings is a design intent question. The code-level mechanics are clear, but Nelson's intent for link behavior under forking — whether links belong to a document identity or a document version — determines whether the current behavior is correct.
Nelson question: When a document is forked (copied to create a new version or variant), should the new document inherit the source document's out-links, or does each document version build its own link set independently?
