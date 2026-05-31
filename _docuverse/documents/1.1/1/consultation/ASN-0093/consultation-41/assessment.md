# Channel Assignment — ASN-0093 review-41

**Date:** 2026-05-31 08:05

## Issue 1: L0 mis-cited for the not-yet-committed key in SubsequentEmissionFreshness
Reason: The fix is internal — the inductive matrix (L14, K.α subsequent-emit) already states the correct citation, and the issue is a self-contradiction within the note resolved by dropping the "L0 /" alternative for the fresh key. No design intent or implementation evidence is at stake.

## Issue 2: Use-site inventory duplicates the per-discipline list that follows it
Reason: Purely editorial deletion of a redundant forward-reference sentence; the per-discipline block already carries the individual ASN-0040 citations. Derivable from the note's own structure.

## Issue 3: Multiple sections defer to the same "chain exhibition" location
Reason: Editorial de-duplication of a deferral pointer in the Properties table; carries no proof obligation and needs no external input.

## Issue 4: Frame preservation over-justified by "state-independence of E(·)"
Reason: Internal simplification — under frame `C' = C` the IH applies directly, so the state-independence citation is decorative; whether the supporting paragraph can be trimmed is checkable against the note's remaining matrix cells alone.
