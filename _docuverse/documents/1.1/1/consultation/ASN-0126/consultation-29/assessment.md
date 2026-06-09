# Channel Assignment — ASN-0126 review-29

**Date:** 2026-06-09 09:15

## Issue 1: Retraction re-expression leaves the attribution source undefined and overstates faithfulness
Reason: Choosing between "declare unattributed retraction inexpressible" and "pin a canonical attribution address" turns on whether anonymous/unattributed retraction is a meaningful distinct operation in the design and whether the implementation attributes deletes — both outside the ASN's own content.
Nelson question: Is an unattributed retraction (no attributing source) intended as a semantically distinct operation, or is attribution always conceptually present and the `F = ∅` form merely a notational default?
Gregory question: Does udanax-green's delete/retraction path carry an attributing source span, or does it emit retractions with no from-set?

## Issue 2: Triple forward-pointer to the same born-nullified witness
Reason: Purely editorial — keep one forward-pointer and delete two. Derivable from the ASN's own structure.

## Issue 3: Duplicated registry-immutability statement
Reason: Editorial deduplication against Registry permanence and P1, both already in the note. Internal.

## Issue 4: `idem` field and P3 carry no in-note role, contradicting the "and only that" scope claim
Reason: The justification ("immutable registry forces all fields to be provisioned at `Σ_init`") is already supplied by the note's own Registry permanence/P1 argument, and the move-to-successor alternative is a scope decision derivable from the note's stated boundaries. Internal.
