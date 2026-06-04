# Channel Assignment — ASN-0087 review-49

**Date:** 2026-06-04 00:57

## Issue 1: `d'` overloaded — "post-state document" vs "other document"
Reason: Pure notation disambiguation — replace the post-state depth uses of `d'` with a state-indexed depth notation and reserve `d'` for non-home documents. Both meanings and the required fix are entirely internal to the note's own definitions.

## Issue 2: Essay flourish in a structural slot ("What Does Not Change")
Reason: Editorial trim — delete the "not a separate guarantee" framing and the closing phenomenology sentence, keep the read-only/spans-not-bytes statement. No design intent or implementation evidence is at stake; the claim M-NoContentEffect is already fully stated by the frame.

## Issue 3: Predictability-of-`ℓ` restated in three places
Reason: Deduplication — consolidate the predictability principle to its load-bearing use in wp Case 2 and let Inputs and the worked example apply it without re-deriving. The derivability of `ℓ` from `A_L(d)` is already established within the note.
