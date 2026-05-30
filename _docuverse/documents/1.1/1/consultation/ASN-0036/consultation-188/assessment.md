# Channel Assignment — ASN-0036 review-188

**Date:** 2026-05-29 22:49

## Issue 1: ShiftPreservation is over-determined by S3 + S7b in its only in-scope use
Reason: The fix is internal — whether ShiftPreservation is redundant turns entirely on the ASN's own proof structure (S8 derives `shift(a,k) ∈ dom(C)` via the lockstep equality and S3 first, after which S7b/S7a/T10a.4 supply the structural shape). No design-intent or implementation evidence is needed; the question of whether any in-ASN use requires structural validity *before* `dom(C)` membership is answerable by inspecting the note's existing lemmas (S7, OrdShiftHom, D-CTG, D-CTG-depth, D-SEQ), none of which consume it.
