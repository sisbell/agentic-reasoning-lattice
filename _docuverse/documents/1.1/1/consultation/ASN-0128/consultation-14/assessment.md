# Channel Assignment — ASN-0128 review-14

**Date:** 2026-06-11 03:06

## Issue 1: The exposed surface's input type contradicts AD's encoding claim
Reason: The note's own weight of evidence (AD, "The operation set," the deferred range-valued-endsets bullet) favors the address-set domain, but locking the signature to address sets is a normative narrowing that should be checked against what the implementation's actual caller-facing surface accepts. Gregory's evidence decides whether the address-set restriction is faithful or whether the endset-typed signature was the honest one.
Gregory question: Does udanax-green's link-creation entry point (CREATELINK) accept endsets as arbitrary span sets carrying content extents, or only whole-entity references — i.e., is the caller-facing surface range-valued or effectively address-valued?

## Issue 2: Three of "the four [R] configurations" are discussed; Multi is silently dropped
Reason: Internal fix. The missing containment argument is fully derivable from material the ASN already cites — the gate sits in `→_sh` itself, so a Binary registration forces single-span to-endsets even on bypass deposits (ASN-0126's P6 form), whereas Multi would admit multi-span to-endsets through the gate. Either eliminating Multi with that sentence or weakening the uniqueness claim requires no external authority.

## Issue 3: BH1's informal Effect overstates the committed rewrite; the filtered-argument boundary is unpinned
Reason: The choice between result-side-only filtering and argument exclusion is a genuine semantic design decision about what lifecycle retirement means, not derivable from the equations (which merely record the narrower commitment). BH1 is a substrate-invented construct with no direct udanax-green analogue, so Nelson's design intent on hiding/visibility is the relevant authority; Gregory has no implementation of filtered views to consult.
Nelson question: When an entity is marked as retired/hidden in the intended design, should it become invisible only in query *results* (enumerations), or should it also stop answering queries posed *about it* — e.g., should asking "what does this retired thing point at" still succeed in the default reader-facing view?

## Issue 4: AM misstates `stale`'s argument
Reason: Internal fix. BH4's own signature in the same note (`stale(h) → set of event-addrs` for an ordinal horizon `h ∈ ℕ`) contradicts the parenthetical; correcting the parenthetical to match is purely mechanical.

## Issue 5: Forward-deferral accretion to AD and DR
Reason: Internal fix. This is a structural reordering/consolidation problem — moving "Denotation and views" before the idem section and the surface-discipline definition plus DR before I4/I6, or consolidating forward pointers — with no semantic content at stake that either authority could inform.

## Issue 6: Defensive authority-appeal prose around already-specified contracts
Reason: Internal fix. The required change is trimming or compressing justificatory prose to one-clause provenance notes; the underlying contracts are already fully specified in the ASN, and no new evidence or intent question is needed to delete defenses of them.

## Issue 7: The operation surface is stated three times
Reason: Internal fix. Consolidating three restatements into one normative signature paragraph, a pointer, and a bare commitments bullet is editorial restructuring of content already present in the ASN; no design-intent or implementation question arises.
