# Channel Assignment — ASN-0070 review-34

**Date:** 2026-06-02 23:14

## Issue 1: The "two halves of the postcondition" fact is stated three times
Reason: Pure editorial deduplication — the fix is to state the split once in the intro and delete the redundant closers. No design intent or implementation evidence bears on where prose is placed.

## Issue 2: Claims Introduced table re-derives proofs instead of indexing them
Reason: Internal formatting fix — trimming table entries to statement and kind requires only the ASN's own content, since the derivations already live in the lemma bodies.

## Issue 3: Directive meta-prose in the V-restricted denotation section
Reason: The definition formula and S8a positivity justification are already present in the ASN; cutting directive prose is a self-contained editorial trim needing no external channel.

## Issue 4: The "Reachability" section restates F-empty in prose
Reason: F0 and F-empty already fix the content formally within the ASN; compressing or deleting a redundant prose preview is derivable internally.

## Issue 5: Interpretive Nelson closers placed inside lemma slots
Reason: The fix is structural relocation — gather interpretive closers into one discussion section. The interpretations are Nelson-attributed motivations, but the revision only moves existing prose; it neither adds new design-intent claims nor verifies them, so it is derivable from the ASN as written.
