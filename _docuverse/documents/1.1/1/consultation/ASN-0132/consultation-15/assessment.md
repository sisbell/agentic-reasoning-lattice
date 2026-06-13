# Channel Assignment — ASN-0132 review-15

**Date:** 2026-06-13 10:37

## Issue 1: The cost scope-decision is stated three times, and the body answers its own open question
Reason: The scope position (cost is QoS, not a correctness obligation) is already settled in the ASN's own text, and the back-end fact the implementation note reports (it pays full enumeration cost) is already stated in the note. The fix is to state the decision once, trim the defensive "we decline... because..." clause, and reframe Q5 to drop its already-answered half — all editorial restructuring of content the ASN already contains, requiring no design intent or implementation evidence.

## Issue 2: Within-document deferrals accrete, and one is a dangling backward reference
Reason: Removing three navigational pointers and opening CN-ORPHAN directly with the count⊇discovery statement is pure cross-reference cleanup; the substantive content (the superset relation) is already present in the next sentence, so the fix is internal.

## Issue 3: CN-UNIT's closing synthesis ends on a circular recap
Reason: Cutting the final self-referential sentence is a one-line editorial deletion; the preceding two-mechanism observation already closes the section, so the fix is derivable from the ASN alone.
