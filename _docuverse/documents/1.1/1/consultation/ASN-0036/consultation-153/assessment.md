# Channel Assignment — ASN-0036 review-153

**Date:** 2026-05-29 02:33

## Issue 1: S8-fin restates "finite" three times
Reason: Pure redundancy removal — collapse three sentences asserting the same proposition into the axiom plus one intent sentence. No design intent or implementation evidence is at stake; the fix is entirely editorial.

## Issue 2: S2 duplicates non-injectivity across postcondition and frame, with a same-document deferral
Reason: Editorial de-duplication within a single Formal Contract — state non-injectivity once in the Frame and drop the "see Frame" pointer. The fact itself (sharing, S5) is already settled in the ASN; nothing external is needed.

## Issue 3: ValidInsertionPosition restates "m is read from state, not a parameter" twice
Reason: Redundancy between Definition prose and Signature; keep one placement. This is a presentation choice fully internal to the ASN.

## Issue 4: S5 vacuous-transition witness needs one sentence of justification
Reason: The required sentence is a logical clarification — that S5 is a non-entailment/consistency result, so a model with no incident transitions is a sufficient witness — derivable from the proof's own structure and the meaning of consistency. No design intent or code evidence is involved.
