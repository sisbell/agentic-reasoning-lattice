# Channel Assignment — ASN-0115 review-15

**Date:** 2026-06-05 07:19

## Issue 1: R9 (CoherentMultiOriginAssembly) has no concrete worked instance
Reason: The fix is internal — adding the worked instance only requires applying definitions and claims already present (R0 `deliver`, R5 ordering, R4 per-document resolution, `origin` and S7 from the substrate section). Constructing two documents `d₁ ≠ d₂` with distinct origins and showing concatenation plus distinct traceable homes parallels the existing R8/R10 instances mechanically; no design intent or implementation evidence is needed.
