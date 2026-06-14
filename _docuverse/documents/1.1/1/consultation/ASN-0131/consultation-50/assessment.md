# Channel Assignment — ASN-0131 review-50

**Date:** 2026-06-14 02:41

## Issue 1: RE-ADDR leans on `wp` Case 2, which governs only triple (`Emit_K`) emissions
Reason: Internal. The arity-independent argument is already written in the note as the discharge of the third conjunct (standing unit-depth discipline + R0a/FlatLinkDomain, both ASN-0086 lemmas already invoked, with R-Scope already flagged "arity-independent"); the fix promotes it to primary and reserves `wp` Case 2 for the genuine triple sub-case (the `Emit_R` emitter `b` in RE-RET), using only already-cited results — no design-intent or implementation evidence is at stake.

## Issue 2: RE-EDIT's shift-based insert/delete coverage rests on the unestablished natural-lift assumption
Reason: Internal. The discharge is a logical observation over ASN-0082's already-established results — its displacement primitives provably write only `Σ.M(d)` and frame `Σ.C`, and since links reference I-addresses (unchanged by V-position displacement, ASN-0043) the lift to the full state frames `L/E/R` by construction; the choice between discharging (a) and deferring (b) is a scoping decision, neither needing fresh evidence.

## Issue 3: Forward-reference accretion around the ASN-0086 bridge
Reason: Internal. Purely editorial — relocating the up-front per-lemma roadmap to its two use sites while keeping the bridge principle; no claim changes.

## Issue 4: Repeated content and defensive asides (anti-bloat)
Reason: Internal. Purely editorial anti-bloat — collapsing the thrice-stated content-identity keying to one, dropping the "not an unresolved question" aside (already carried by RE-UDIST-∩/OQ4), and trimming meta-narration; no claim changes.
