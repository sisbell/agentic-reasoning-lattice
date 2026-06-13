# Channel Assignment — ASN-0108 review-41

**Date:** 2026-06-13 06:11

## Issue 1: W5's sufficiency argument for the central coherence guarantee is a sketch
Reason: Internal. The fix is to complete or signpost the chaining argument using material already present — W9b's cursor-advance induction (no re-delivery) and W9's `After(final) = ∅` local fact (delivery under termination); no design intent or implementation evidence is at issue, and the reviewer flags it as a precision/pointer fix.

## Issue 2: Forward-preview accretion in the `Match` definition
Reason: Internal. Pure editorial restructuring — name M-fin and M-mut as the standing handles and let W6a introduce the K.λ-increment at its sole use site; all three facts already live in the note.

## Issue 3: W6 restates the injectivity caveat as an orthogonal digression
Reason: Internal. The fix deletes a restatement of the non-injectivity point already established in the "What `κ` is" / W1 discussion; nothing new is needed from either channel.

## Issue 4: W6a's functional characterization excludes a key it claims to cover
Reason: Internal. The note already defines the content-position key as the current V-position in the consulted arrangement `Σ.M(d_q)` and supplies the M/C frame justification, so reconciling the functional form (to "(address, boundary or position)" or "reads only `(address, Σ.M(d_q), Σ.C)`") is derivable from the ASN's own definitions.
