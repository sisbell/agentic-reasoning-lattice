# Channel Assignment — ASN-0100 review-75

**Date:** 2026-06-05 04:23

## Issue 1: INS.alloc claim row cites the wrong freshness lemma
Reason: Internal — the body (Effect One, §Atomicity S4 bullet) already discharges K.α's freshness via SubsequentEmissionFreshness + FirstEmissionFreshness; the fix is a mechanical citation correction in the claim row to match the body.

## Issue 2: Proof of INS.M-exhaustive embedded in the Formal Contract slot
Reason: Internal — the exhaustiveness justification already exists in the ASN and is reused in §Verifying the Invariants; the fix relocates existing prose, no design or implementation input needed.

## Issue 3: Duplicate coupling-discharge prose across the two worked examples
Reason: Internal — the general J0/J1★/J1'★ discharge is already in §Provenance; the fix removes a near-verbatim restatement, purely editorial.

## Issue 4: Effect Three frame enumeration duplicates the Formal Contract Frame Conditions
Reason: Internal — the same four frame facts appear formally under §Frame Conditions; the fix trims Effect Three to discovery-level observations, no external evidence required.
