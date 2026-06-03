# Channel Assignment — ASN-0075 review-40

**Date:** 2026-06-03 07:46

## Issue 1: D-DISCR's claimed implementation-obligation is stronger than the lemma proved
Reason: Internal. The bridge from insufficiency to obligation is a one-step logical derivation using only this ASN's own definitions: SHOWDELETIONS requires the DELETED/NEVER_INCLUDED distinction, the `Σ_1`/`Σ_2` witnesses prove `(C,L,E,M)` cannot supply it, so any implementing state needs extra components, and the DELETED/NEVER_INCLUDED definitions show `R`-membership alone suffices. No design intent or implementation evidence is consulted.

## Issue 2: First edge case duplicates the Q0 weakest-precondition derivation verbatim
Reason: Internal. This is a pure redundancy cut — the edge-case bullet restates the already-derived `wp(SHOWDELETIONS, Q0)` formula. Removing or back-pointing requires only comparing two passages within the ASN.

## Issue 3: D-ACT restates D-IDENT and fills its justification with forward-looking speculation
Reason: Internal. The substantive content (output ⊆ `dom(C)`, consumable as I-addresses) already follows from the definition and D-IDENT; trimming the speculative "not wrapped in V-positions/values" prose is a structural-discipline edit derivable from the ASN's own claims.
