# Channel Assignment — ASN-0131 review-62

**Date:** 2026-06-14 06:31

## Issue 1: RE-ADDR — "the only to-set that could cover ℓ_new is its own" omits the step that makes it true
Reason: Internal fix. The reviewer has already pinpointed the missing inference and the foundation property that discharges it — ASN-0086's Nullify P-tgt (pre-existing retraction targets lie in `dom(Σ.L)`, hence differ from the fresh `ℓ_new ∉ dom(Σ.L)`); this is a derivation gap closed by citing an already-established property the note builds on, not a question of design intent or implementation behavior.

## Issue 2: anti-bloat — consumer-enumeration scope-note and bridge method-narration
Reason: Internal fix. Pure prose surgery — cut the consumer-enumeration sentence, compress the bridge to its load-bearing inclusion (`K.σ`-registrability + `K.λ`-replay), and relocate the empty-from-set fact to its use in RE-RET; all content is already present in the note and nothing turns on Nelson's intent or Gregory's evidence.
