# Channel Assignment — ASN-0086 review-236

**Date:** 2026-06-01 20:36

## Issue 1: Nullify's Effect clause overstates `a ∈ nullified(Σ')`
Reason: The corrected condition `P1 ∨ (a = a_emit(Σ, d_retr))` is already derived as the weakest precondition in wp Case 1 of the ASN itself; the fix is internal, just aligning the Effect clause with the note's own result.

## Issue 2: Repeated forward-deference to "wp Case 1, self-emit branch"
Reason: Purely editorial consolidation of redundant cross-references to a proof already present in the ASN; no design intent or implementation evidence is needed.

## Issue 3: Anticipatory meta-prose in the Nullify precondition paragraph
Reason: Editorial reduction to operative facts; the preconditions and R0's on-chain guarantee are already established within the ASN, so trimming the rationale is internal.

## Issue 4: Essay content in Definition — TupleAddress
Reason: A placement fix relocating motivational prose out of a definition slot; the definition of `addr` is already complete in the ASN, so no external channel is required.
