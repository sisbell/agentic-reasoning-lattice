# Channel Assignment — ASN-0036 review-185

**Date:** 2026-05-29 22:20

## Issue 1: TS3 cited at the i = 0 boundary where its precondition fails
Reason: The fix is internal — the `shift(t,0) := t` convention (already stated in S8's preconditions) discharges the `i = 0` case and TS3's `n ≥ 1` precondition applies for `i ≥ 1`. Splitting the induction step uses only material already present in the ASN.

## Issue 2: ShiftPreservation mis-attributed as establishing dom(C) membership
Reason: The fix is internal — the correct attribution (membership via the lockstep equality and S3, ShiftPreservation for structure only) is already stated verbatim elsewhere in the same proof body and in contract postcondition (a). Reconciling the conjunct-(b) prose needs no external evidence.

## Issue 3: Ordinal-decomposition machinery introduced but not consumed
Reason: The fix is internal — the reviewer already demonstrates OrdShiftHom (b),(c) reduce to direct `OrdinalShift`/`TumblerAdd` facts about `δ(n,m)`, and which lemmas S8's proof actually consumes is determinable from the ASN's own dependency structure. Choosing trim-vs-move is an authorial scope decision, not a question of design intent or implementation behavior.

## Issue 4: Duplicate framing sentence across S8 section
Reason: The fix is internal — purely an editorial deduplication of two sentences asserting the same point within one section.

## Issue 5: Roadmap prose enumerating downstream lemmas
Reason: The fix is internal — removing meta-prose that previews downstream lemmas requires only editing within the ASN; no design or implementation input bears on it.
