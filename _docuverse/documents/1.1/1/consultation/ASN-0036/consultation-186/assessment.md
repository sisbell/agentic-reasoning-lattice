# Channel Assignment — ASN-0036 review-186

**Date:** 2026-05-29 22:33

## Issue 1: OrdShiftHom labeled (b) and (c) with no (a)
Reason: Pure relabeling residue from the recorded collapse; the fix (renumber to (a)/(b) or note the dropped (a)) is derivable from the ASN's own structure and git history without design intent or implementation evidence.

## Issue 2: S7c, `subspace_I`, and ShiftPreservation (iii)/(iv) have no in-ASN consumer
Reason: Whether any in-ASN claim consumes (iii)/(iv)/S7c is a purely textual audit of this note, and the note's own Open Questions already defer subspace alignment to the operations layer — so removal is justified internally without consulting either channel.

## Issue 3: Coined label "Nat-pos"
Reason: Dropping the invented name and citing NAT-discrete directly is a mechanical editorial fix; the foundation vocabulary referenced is already present in the ASN.

## Issue 4: S8 partition does not address the empty arrangement
Reason: The empty case is vacuously true under the existing orbit construction; adding the one-sentence statement is derivable from the proof already in the ASN.

## Issue 5: Editorializing in the S8 lead
Reason: Cutting the self-importance assertion to the structural statement is an editorial fix internal to the note.
