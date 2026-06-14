# Channel Assignment — ASN-0134 review-42

**Date:** 2026-06-14 12:49

## Issue 1: The K.σ registration conflict is assumed away, not eliminated — `register-before-allocate` is named but `register-vs-register` is dropped
Reason: The fix turns on whether account→document allocation is itself an owned, serialized sub-allocator (making the same-target registration race the H2/clause-2 discipline one level up) or an externally-proposed `d` merely checked against `dom(M)`. The note models `K.σ` only as a flat `dom(M)` freshness check and defers the `A_doc` layer to "the entity-allocation layer," so the structural-isomorphism claim is not internally derivable — it needs the intended allocation structure (Nelson) with implementation corroboration of the collision (Gregory).
Nelson question: In the owned-numbers design, does an account own and serially allocate its document numbers as a sub-allocator — so two concurrent document creations under one account contend exactly as two content writers under one document do — or are document addresses proposed externally and only checked for uniqueness?
Gregory question: In udanax-green, how is a new document/orgl tumbler allocated under an account — is it drawn from a frontier-style sub-allocator so two concurrent same-account creations would collide on one address (as content allocations do), and what becomes of the loser?

## Issue 2: V2's "weakest sufficient condition" mis-scopes `Q`-affecting steps for a cross-type join — nullifications are omitted
Reason: Internal — the correction follows directly from the note's own definition of `Q`-affecting (any step changing a not-yet-read `c_i`) together with `A_{K_i} = L_{K_i} ∖ nullified` and §4's established fact that a nullifier's emitter is homed at an arbitrary `d_retr`; a nullify hitting an active `K_i` tuple is therefore `Q`-affecting regardless of its home, by the note's own machinery alone.

## Issue 3: Anti-bloat — meta-prose around A0 and a forward use-site inventory in the intro
Reason: Internal — pure prose surgery; the Nelson-intent content being trimmed (A6/W0/V0 grounding) is already stated at its use-sites, so cutting the role/importance framing, the forward use-site tags, and the self-referential sentence requires no external input.
