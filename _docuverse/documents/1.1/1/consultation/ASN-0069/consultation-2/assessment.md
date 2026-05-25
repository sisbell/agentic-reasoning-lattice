# Channel Assignment — ASN-0069 review-2

**Date:** 2026-05-25 12:20

## Issue 1: V1's formula is only correct for the first fork
Reason: Fix is derivable from ASN-0047's Allocator hierarchy, which already specifies the chain-advancement convention (`inc(d, 1)` first, `inc(prev_version, 0)` after). Generalizing V1, V0, and the composite verification requires only re-applying that convention plus K.δ's case (i)/(ii) selection — no external evidence or design-intent question.

## Issue 2: V7's K.δ-alone composite is not a J4 composite
Reason: This is a framing question about how to locate V7's composite shape relative to J4 — extension vs. relaxation. The substantive design decision (empty-source forks are normative) is already grounded in the cited LM 4/66 and CREATENEWDOCUMENT precedent. The fix is internal presentation rigor.

## Issue 3: V2's derivation only handles first-fork case
Reason: The chained-`inc(·, 0)` derivation invokes TA5(b)'s k=0 clause and TA5-SigValid, both already established in ASN-0034. No external input needed; just spell out the induction over chain-advancement steps.

## Issue 4: V8c's derivation is hand-waved
Reason: Pure derivation cleanup. Cite V8 for one direction and symmetry of equality for the other — both are inside the ASN.

## Issue 5: V11's derivation lacks induction structure
Reason: Formalize induction using V4 (per-step equality) and V5 (per-step source isolation), both already established in this ASN. Internal.

## Issue 6: K.ρ multiplicity in the composite is left informal
Reason: K.ρ's per-invocation semantics and ValidComposite★'s per-step discharge conditions are defined in ASN-0047. Making the n-fold K.ρ structure explicit is a matter of formal accounting against the existing framework, not new evidence or intent.
