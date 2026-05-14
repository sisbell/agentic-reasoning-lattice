# Channel Assignment — ASN-0058 review-21

**Date:** 2026-05-13 20:19

## Issue 1: M-sub clause (a) is false for #v = 1
Reason: The fix is derivable from the ASN's existing framework — the proof of M7 already notes "m ≥ 2 (V-positions in M(d) lie in the element subspace)", and S8-depth/S7c commit V-positions in arrangements to depth ≥ 2. The reviser only needs to decide between adding a precondition to M-sub (a) and tightening the mapping block definition; no external evidence or design intent is required.

## Issue 2: M7 necessity proof conflates abstract and decomposition contexts
Reason: This is a proof-restructuring issue with two clean internal options already laid out in the finding — either precondition the necessity claim on β₁, β₂ ∈ B, or derive each case from ⟦β₁ ⊞ β₂⟧ = ⟦β₁⟧ ∪ ⟦β₂⟧ alone. Both routes use only existing ASN content.

## Issue 3: C1a generalization needs explicit depth bound
Reason: The proof already cites OrdShiftHom's #v ≥ 2 precondition; the fix is to surface that bound in the statement of (iii). Pure tightening of an under-specified condition against an established dependency.

## Issue 4: C0b numbering is out of sequence
Reason: Pure organizational/numbering fix. The dependency graph (C0b → C1a) is visible in the ASN itself, so the reviser can choose the renumbering or relocation locally.

## Issue 5: M2 preconditions are inherited but never stated
Reason: The inherited preconditions (S8-fin, S2, S3, S8a, S8-depth, S7b, S7c) are explicitly enumerated in the finding itself and live in ASN-0036. Transcription, not inquiry.

## Issue 6: M0's proof does not address n = 1
Reason: Trivial base-case annotation; the n = 1 conclusion (V(β) = {v}, |V(β)| = 1) follows immediately from the definition with no further structure needed.
