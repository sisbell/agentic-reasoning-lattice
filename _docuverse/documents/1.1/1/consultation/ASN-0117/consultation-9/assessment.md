# Channel Assignment — ASN-0117 review-9

**Date:** 2026-06-08 22:56

## Issue 1: The K.μ⁻ + K.μ⁺ composite decomposition fails when the suffix is empty (R = ∅)
Reason: Internal fix. The case split is fully determined by definitions already in the ASN — the K.μ⁺ strict-extension precondition (ASN-0047), the J2 ContractionIsolation self-sufficiency of a lone K.μ⁻, and the ASN's own `R = ∅` arithmetic (`N − c = J − 1`). No design intent or implementation evidence is needed to restate the decomposition as a case split and re-discharge the single-step coupling/frame obligations.

## Issue 2: The R = ∅ worked examples are inconsistent with the stated Effect
Reason: Internal fix. Same root as Issue 1; once the case split is stated, annotating the two boundary examples and re-confirming the invariant appeals (S3★, DEL-FENT, DEL-FPROV, P4★, P7a) for the single-step K.μ⁻ realization follows mechanically from the ASN's own clauses and the cited ASN-0047/0098 properties.
