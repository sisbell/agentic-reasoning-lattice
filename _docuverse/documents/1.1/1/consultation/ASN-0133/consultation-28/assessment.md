# Channel Assignment — ASN-0133 review-28

**Date:** 2026-06-14 04:54

## Issue 1: The unconditional-recognizability claim is stated twice with the same triple
Reason: Pure within-note deduplication — both statements are already present in the ASN; consolidating the "undisciplined/unfair/divergent" triple into Q1 and trimming the Triggers paragraph to the PR-DISC caveat is mechanical text editing that turns on no design intent or implementation behavior.

## Issue 2: Q6's closing sentence restates Q5a's checkability breakdown
Reason: Internal restructuring — both passages live in the note; keeping Q6's "not a third hypothesis of Q6" line and replacing the duplicated checkability breakdown with a citation to Q5a is derivable from the ASN's own content alone.

## Issue 3: The H-ATOM single-tuple point is repeated in "What this note doesn't cover"
Reason: Pure deduplication — the deferral bullet re-derives H-ATOM's own already-established result (single-step fires atomic-for-free by I4); dropping the parenthetical and deferring only the scheduler/serialization model is internal to the note.

## Issue 4: "settled there" directs the reader to an unresolved open question
Reason: Cross-reference disposition correction — whether ASN-0130's Open Question 3 is "settled" or "open" is a documentary fact about a cited dependency, already confirmed open by the reviewer; the load-bearing claim (PR3 reads content not registration) is self-contained, so no design-intent or implementation evidence is required.

## Issue 5: Same set called both "upward" and "downward" closure
Reason: Terminology self-consistency — the `≼`/coverage convention is fixed by the note's own usage and its dependency ASN-0086; the reviewer confirms the math is unambiguous, so picking one direction word for the `≼`-extension set is derivable internally without Nelson or Gregory.
