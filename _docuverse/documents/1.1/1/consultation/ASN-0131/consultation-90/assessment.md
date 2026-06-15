# Channel Assignment — ASN-0131 review-90

**Date:** 2026-06-14 18:28

## Issue 1: Unit-depth confinement rationale stated twice
Reason: Pure prose-deduplication internal to the ASN — the fix is to delete a forward-looking closing sentence in the RE-NCD block because the identical confinement fact ("coverage reduces to `s ≼ c`, hence unit-depth only") is re-derived at its point of use in the retraction subsection. Both statements of the fact already live in the note; no design intent or implementation evidence is at stake.

## Issue 2: "No injectivity-style restriction recovers ⊇" previewed, then proved, then restated
Reason: Pure structural-deduplication internal to the ASN — the fix removes a preview clause that states obstruction 2's earned conclusion three times, leaving the injective construction to carry the headline once where it is proved. The mathematical content (both obstructions, the injective counterexample) is already present and correct; the choice is editorial, requiring neither design intent nor implementation evidence.
