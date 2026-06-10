# Channel Assignment — ASN-0126 review-87

**Date:** 2026-06-10 03:43

## Issue 1: The operation-set claim conflates operations with transition steps, and lists an operation the gate makes unreachable
Reason: The fix is internal. The operation/transition-step distinction is already drawn in the note — `→_sh ≡ K.σ ∪ K.α ∪ K.λ_sh` (The shape-gated emit), with `K.λ_sh` listed among the *transition steps* and given a frame condition (Registry permanence). Both reconciling facts are already proven within the note: `Nullify`'s lack of a `→_sh` image (The shape-gated emit) and its re-expression as a from-filled Binary `Emit_R` (Retraction as an attributed Binary). Aligning the one offending sentence requires only self-consistency — no design intent or implementation evidence.
