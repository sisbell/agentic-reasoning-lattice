# Channel Assignment — ASN-0131 review-49

**Date:** 2026-06-14 02:15

## Issue 1: The ASN-0086 bridge does not license the two ASN-0086 lemmas it is invoked for
Reason: Internal/formal fix. The correction is purely about the dependency lattice's structure — that `dom(Σ.M) = E_doc` is the shared ASN-0093 document substrate both ASN-0086 and ASN-0047 extend, so the document operand and `a_emit` are the same object under either transition relation. The reviewer has already supplied the correct reasoning; broadening the bridge (or re-deriving the `dom(Σ.M)`-touching hypotheses inline) draws only on the formal content of cited dependencies, not on Nelson's design intent or Gregory's implementation evidence.

## Issue 2: Forward-reference accretion and defensive scoping prose (anti-bloat)
Reason: Internal/editorial fix. Hoisting the non-self-targeting fresh-`K.λ`-output addressability fact into a named lemma and removing the worked instance's meta-commentary are pure restructurings of content already present and proved in the note. No design intent or implementation evidence is required.
