# Revision Categorization — ASN-0025 review-3

**Date:** 2026-03-07 07:48

## Issue 1: State model codomain excludes structural allocations
Category: INTERNAL
Reason: The review itself notes "no argument actually depends on the codomain being `Byte`" and "the fix is a definition change, not an argument change." The ASN already describes what CREATE VERSION, CREATE DOCUMENT, and CREATE LINK allocate — generalizing the codomain from `Byte` to `Value` is derivable from the ASN's own content.

## Issue 2: CREATE LINK has conditional J0 verification and no document target
Category: BOTH
Reason: The ASN already implies links have V-space presence (DELETE section mentions "links at 2.x") but never specifies which document receives a link entry. Resolving this requires Nelson's design intent on whether every link belongs to a specific document, and Gregory's implementation evidence for which document the code targets.
Nelson question: When a link is created between spans in two documents, does Nelson's design require the link to reside in a specific document's V-space (e.g., the creating user's document), or can links exist in I-space without any V-space representation?
Gregory question: In the implementation, when `docreatelink` (or equivalent) creates a link, which document's POOM receives the link entry at element prefix 2.x — and is it always exactly one document?

## Issue 3: Structural consequences depend on unmodeled link state
Category: INTERNAL
Reason: The fix is editorial: either present link survivability as conditional on a future link ASN (option b from the review), or add a minimal `Σ.links` component using information already stated in the ASN. No new external evidence is needed — the ASN already establishes that links reference I-space addresses from Nelson and Gregory; the gap is purely in the formalization choice.
