# Channel Assignment — ASN-0128 review-29

**Date:** 2026-06-11 08:26

## Issue 1: I6's necessity argument silently relies on the attainability convention that DR states explicitly
Reason: The fix is internal — the attainability convention and the per-precondition necessity split are both already stated in DR within this note, and the review prescribes the exact repair (import the convention at I6's wp display and split the rejected-call case from the admitted-miss-failing-C3 case). No design intent or implementation evidence bears on a proof-bookkeeping alignment between two sections of the same note.

## Issue 2: The I5 ↔ I6-corollary relationship is stated three times in three consecutive blocks
Reason: Purely editorial — the review identifies which of the three statements carries content and directs deleting I5's closing sentence while keeping at most the exposed-signature pointer. The fix changes no semantics, so neither channel is needed.
