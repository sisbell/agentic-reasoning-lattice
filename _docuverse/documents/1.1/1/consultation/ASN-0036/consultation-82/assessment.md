# Channel Assignment — ASN-0036 review-82

**Date:** 2026-05-11 01:54

## Issue 1: S7a's axiom uses projections that S7b is needed to make total
Reason: Internal fix — reorganize S7a's dependencies or statement to make the structural premise (zeros(a) ≥ 2 or 3) explicit. The content is already present in the ASN; this is a structural ordering issue between S7a and S7b.

## Issue 2: S8's formal contract lacks a *Depends* section
Reason: Internal fix — the dependencies are enumerated in the proof body and Properties Introduced table; the fix is to copy them into a *Depends* section for self-containment.

## Issue 3: D-CTG-depth's formal contract lacks *Depends*
Reason: Internal fix — the proof body and Properties Introduced table already enumerate the consumed claims (T0(a), T1, T3, S8a, S8-fin, S8-depth, D-CTG); the fix is structural.

## Issue 4: D-SEQ's formal contract lacks *Depends*
Reason: Internal fix — proof body lists the dependencies (D-CTG, D-CTG-depth, D-MIN, S8a, S8-fin, S8-depth, T1); the fix is to add a *Depends* section.

## Issue 5: S5's formal contract lacks *Depends*
Reason: Internal fix — the construction verifies S0–S3 vacuously/non-trivially and uses T3 and carrier-membership reasoning; these are visible in the proof and need only be transcribed into a *Depends* section.

## Issue 6: S8a's positivity step appeals to NAT-zero without citation
Reason: Internal citation fix — NAT-zero (NatZeroMinimum) is a foundation claim in ASN-0034 that the proof implicitly uses; adding the citation is a mechanical foundation-hygiene correction.
