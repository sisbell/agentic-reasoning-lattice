# Channel Assignment — ASN-0086 review-214

**Date:** 2026-06-01 17:03

## Issue 1: M2 / empty-arrangement derivation is consumed by no claim
Reason: The fix is a deletion of unused derivation prose; the finding already establishes nothing in the note consumes M2, and the replacement sentence is noted as already present. Purely internal editorial cleanup.

## Issue 2: The `a_emit` emission rule is restated in three places
Reason: Consolidating a verbatim restatement to a single formal definition plus by-name citations is an internal editorial move; the canonical rule already lives in Definition — `a_emit`.

## Issue 3: `T_ghost^Σ` is defined but never consumed
Reason: The finding confirms no claim references the set; deleting or folding it into the existing L9 prose is derivable from the note's own content with no need for design intent or implementation evidence.

## Issue 4: Forward pointers used where a citation would do
Reason: Dropping the multi-arity parenthetical (already in Open Questions) and removing the inline `~` preview ahead of its own definition are self-contained editorial fixes internal to the note.
