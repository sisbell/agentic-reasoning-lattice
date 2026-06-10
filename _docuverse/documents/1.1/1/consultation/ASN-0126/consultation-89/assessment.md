# Channel Assignment — ASN-0126 review-89

**Date:** 2026-06-10 04:20

## Issue 1: The declared operation set lists an inherited `Nullify` that has no `→_sh` image
Reason: Internal. The note already proves both halves of the fix — that inherited empty-from `Nullify` has no `→_sh` image ("The shape-gated emit") and that retraction is re-expressed as the Binary `Emit_R` wrapper ("Retraction as an attributed Binary"). Reconciling the operation-set declaration with `→_sh` is a presentation choice between two options both fully supported by the note's own content; no design intent or implementation evidence is in question.

## Issue 2: "K.σ and K.α are unchanged" is contradicted by the registry-framing added later
Reason: Internal. Both conflicting statements live in the note ("The shape-gated emit" vs. "Registry permanence"), and the intended claim — preconditions and C/M/L effects unchanged, registry additionally framed — is already established by P1's proof. The fix is a wording qualification the review itself supplies; no external channel is needed.
