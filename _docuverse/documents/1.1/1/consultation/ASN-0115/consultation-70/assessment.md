# Channel Assignment — ASN-0115 review-70

**Date:** 2026-06-10 22:28

## Issue 1: Deep-case emptiness argument applies Confinement beyond its stated form
Reason: The fix is a purely internal proof repair — strengthening Confinement's postcondition to record the length consequence (`p ≼ t`, hence `#t ≥ m − 1`) and splitting the deep case into the two sub-cases the review identifies. All needed material (TumblerAdd, T5, T1, S8-depth) is already cited in the ASN; no design intent or implementation evidence bears on it.

## Issue 2: R7 proof defends its hypothesis against a case the carrier excludes
Reason: The required fix is deletion of prose after "The hypothesis gives `Σ →* Σ'` directly", which is derivable from the ASN's own standing precondition (sequential transition order) — the divergent-branch case is excluded by the carrier, so no reconciliation question actually arises. Internal.

## Issue 3: R11 wp paragraph states the same discharge twice in adjacent sentences
Reason: Pure redundancy removal — keep one of two equivalent formulations of the S3★/S0 discharge. No external input needed.

## Issue 4: R8's no-deduplication point is made twice in one paragraph
Reason: Pure redundancy removal — state the R3-forces-both point once around the existing Gregory evidence sentence. The implementation fact (absent `consolidatespans`) is already established in the ASN; no new evidence needed.

## Issue 5: R2 uses an undefined projection `.val`
Reason: Notational repair derivable from the ASN's own `item` definition — either define the value projection on content-tagged items or restate R2 as the tagged-pair equality, as the claims table already does informally. Internal.
