# Channel Assignment — ASN-0126 review-74

**Date:** 2026-06-09 23:42

## Issue 1: The `name` registry field is unconstrained and unread
Reason: Internal. The note already commits type identity to coverage class (inherited ASN-0086 TypeEquivalence) and exhibits no framework machinery that reads `name` — gate, `shape(·)`, and `Sh-conf` read only shape and span counts. Both resolution paths (declare it uninterpreted app metadata and drop "identifier," or add a uniqueness invariant with a named reader) are decidable from these commitments already in the note; the absence of any internal reader forces the metadata route, justifiable as the registry's app-declaration payload without new design-intent or implementation facts.

## Issue 2: The B2-exclusion paragraph inventories two results the note never uses
Reason: Internal. Which existence-of-successor results this note actually lifts is a fact about its own argument — only R0 is re-derived, as P5 — so dropping the R5/R6c references or genericizing the exclusion is a self-contained edit needing no external evidence.

## Issue 3: P2 (ShapeStability) is stated, listed, never cited, and re-derived inline
Reason: Internal. Whether P2 is cited anywhere and whether P4 re-derives its content are facts about the note's own dependency structure; choosing to cite P2 at P4's use site or remove it and let P1 carry the weight is pure internal restructuring.

## Issue 4: The "Sh-conf is partial / undefined for unregistered K" gloss is re-explained three times
Reason: Internal. The partiality of `Sh-conf` is defined within the note itself; consolidating the three restatements into one canonical definition plus by-reference invocations is an editorial change entirely on the note's own content.
