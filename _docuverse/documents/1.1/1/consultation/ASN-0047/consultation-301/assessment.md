# Channel Assignment — ASN-0047 review-301

**Date:** 2026-06-01 23:22

## Issue 1: J4 fork range bound is weaker than the version-copy semantics it claims
Reason: Deciding whether a version-fork must copy *all* source content (range equality) or may drop content (subset) turns on design intent (is CREATENEWVERSION meant to be a faithful full copy?) and implementation behavior (does the code copy the whole POOM or admit partial copies?). Both channels bear on the (a)-vs-(b) choice.
Nelson question: Is CREATENEWVERSION intended to produce a complete copy of the source document's current contents, or may a new version deliberately include only a portion of the source's content?
Gregory question: Does `docreatenewversion` copy the source document's entire content arrangement (full POOM), or can it produce a version whose arrangement contains only a subset of the source's content addresses?

## Issue 2: Class (a) matrix S3★/K.μ~ cell is essay-length, re-deriving rather than indexing
Reason: Purely editorial — the fix replaces inline re-derivation with a pointer to Step (B), which already exists in the ASN body; derivable from the ASN alone.

## Issue 3: FrontierEquivalence is re-glossed at every invocation
Reason: Purely editorial — strip the repeated definitional parenthetical and consolidate the K.δ case (ii) discharge into one owning location; all content already present in the ASN.
