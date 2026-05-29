# Channel Assignment — ASN-0036 review-144

**Date:** 2026-05-29 01:33

## Issue 1: Citations to a dissolved "ordinal-shift prefix lemma"
Reason: Internal — the fix substitutes a phantom lemma name with OrdinalShift (ASN-0034), whose postconditions are already cited in the Depends lists; no design intent or implementation evidence is needed.

## Issue 2: S8 partition proof omits the empty-arrangement boundary
Reason: Internal — the empty case follows vacuously from the proof's own structure (S8-fin, vacuous quantification); naming it requires no external input.

## Issue 3 (anti-bloat): Downstream-consumer justification in D-CTG
Reason: Internal — a pure deletion of a sentence whose content is already established locally in the D-CTG-depth and D-SEQ proofs.

## Issue 4 (anti-bloat): S3 one-directionality stated twice; S8a forward-justifies S8-depth
Reason: Internal — trimming duplicated prose and a forward-justification clause; both edits are within the ASN's existing material.
