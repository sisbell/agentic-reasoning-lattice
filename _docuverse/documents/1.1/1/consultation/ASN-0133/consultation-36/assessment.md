# Channel Assignment — ASN-0133 review-36

**Date:** 2026-06-14 11:26

## Issue 1: the Marker-pattern definition enumerates its downstream consumers
Reason: Pure prose-editing fix — the Marker pattern's substantive definition (negated-existential trigger, emit-the-witness contract) is already fully stated in the same sentence; removing the downstream-consumer parenthetical and self-description requires no design intent or implementation evidence.

## Issue 2: the per-occurrence reading is justified by a use-site inventory
Reason: Internal deletion — the per-occurrence definition stands complete on its own (through "across a later tail"); cutting the trailing use-site inventory is mechanical and needs no external channel.

## Issue 3: the Marker-pattern at-most-once mechanism is re-spelled at each use
Reason: DRY/deduplication fix internal to the note — the mechanism is already stated in full at Q-EXT, so replacing Q5a's re-spelling with a citation is derivable from the ASN's own content.

## Issue 4: confusing trailing self-reference in the pdef-trigger conditionality note
Reason: Prose-clarity fix about the Q0/Q1 conditionality relationship, all internal to the ASN; the review even supplies the exact rewrite, so no design intent or implementation evidence is needed.

## Issue 5: the intro thesis restates the subtitle
Reason: Internal redundancy removal — the substantive fact is carried by the preceding sentence and the subtitle, so deleting the duplicate self-referential sentence requires nothing external.
