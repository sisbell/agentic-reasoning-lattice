# Channel Assignment — ASN-0132 review-11

**Date:** 2026-06-13 08:49

## Issue 1: CN-RETRACT's prose contradicts CN-RETRACT
Reason: Internal. The fix is a pure deletion of a clause that contradicts the ASN's own machinery — CN-RETRACT states nullified contributes `0` "for every `q`," and CN-DEF filters `addressable(Σ)` before `sat`/`liftH` is reached, with global nullification cited from R6a (ASN-0086) and FL-RET (ASN-0121). No design-intent or implementation evidence is needed to remove a clause the ASN's definitions already falsify.

## Issue 2: CN-SNAP's implementation note asserts deferred federation semantics
Reason: Internal. The fix is subtractive — trim the distributed/replicated-model assertion back to CN-SNAP's single-state point ("count is a function of whichever `Σ` is observed"), which is already CN-SNAP itself. The ASN explicitly declares federation out of scope and defers it to an open question, so removing the overreach requires no new implementation fact from Gregory.

## Issue 3: Placement-justification and prompt-framing meta-prose
Reason: Internal. Pure prose rephrasing; the substantive content (permanence guarantees existence, not reported counts) is already present and correct in the ASN. Dropping the placement-justification and "the question" connectives needs no channel.

## Issue 4: Resolution principle restated rather than referenced (minor)
Reason: Internal. Pure cross-reference fix; the resolution principle is already established in the ASN's "A remark on the request as given" section, so CN-STAB's caveat can point back to it rather than restate it. No channel needed.
