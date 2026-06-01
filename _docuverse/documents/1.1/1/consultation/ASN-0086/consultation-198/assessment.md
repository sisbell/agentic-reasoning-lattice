# Channel Assignment — ASN-0086 review-198

**Date:** 2026-06-01 14:29

## Issue 1: `a_emit` is defined as "the address K.λ deposits" but is actually a total formula that yields a value where K.λ has no valid edge
Reason: The fix is a definitional choice between two readings already laid out in the note's own machinery (the total first/subsequent formula vs. the partial K.λ-edge domain); no design intent or implementation evidence is needed to pick one and re-state Emit_K's commitment separately.

## Issue 2: Meta-commentary on proof structure inside the K-Step Conformance Preservation proof
Reason: Pure editorial deletion of self-narration; the clause-by-clause discharge already present in the proof is the content, so the fix is internal.

## Issue 3: Lemma — Emit_K function-ness largely restates Definition — `a_emit`
Reason: Whether to fold the lemma into Definition — Emit_K or cite a downstream consumer is decidable by inspecting the note's own cross-references; no external channel bears on it.
