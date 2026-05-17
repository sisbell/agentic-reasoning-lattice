# Channel Assignment — ASN-0047 review-68

**Date:** 2026-05-17 02:13

## Issue 1: K.μ⁺_L's "S8" verification incorrectly extends ASN-0036's S8 to the link subspace
Reason: Self-contained. The correct treatment already exists later in this ASN under "S8-scope in the extended state" — the fix is to align the K.μ⁺_L paragraph with that scoping (project S8 to content subspace; cite per-subspace D-SEQ★ for the link subspace).

## Issue 2: K.δ effect for IsNode case lacks explicit M-clause
Reason: Self-contained presentational fix. The frame clause plus totality convention already determine the behavior; the rewrite only needs to make IsNode/IsAccount M-handling explicit and distinguish frame-implied empty from semantic activation in the IsDocument case.

## Issue 3: ExtendedReachableStateInvariants per-state list omits P4a
Reason: Self-contained bookkeeping. P4a's derivation already exists in the body; the fix is to add it to the conjunct list and note that its preservation follows from the existing P2 + J1'★ chain.

## Issue 4: D-SEQ★ forward pointer relies on a circularity disclaimer that doesn't fully discharge
Reason: Self-contained proof-structure clarification. The inductive structure is standard and recoverable from the ExtendedReachableStateInvariants induction already in the ASN; the fix is to make the inductive hypothesis explicit in the disclaimer.

## Issue 5: K.μ~ contract's "subspace-preserving" admissibility constraint is asserted but not derived
Reason: Self-contained formal question. Subspace-preservation is derivable from the bijection equation + pre/post-state S3★ + L14 using the same chain as link-fixity; the fix is to either derive it (eliminating the constraint) or articulate the asymmetric treatment.

## Issue 6: Bootstrap node n₀'s structural specification has minor inconsistency
Reason: Nelson can clarify whether the value `1` specifically (vs. any single-component positive tumbler) is structurally load-bearing or a convention. The existing LM 4/28 citation establishes the convention; the question is whether `[5]` or `[42]` would be formally equivalent or design-incompatible.
Nelson question: Is the choice n₀ = [1] structurally necessary for your design — does the specific digit "1" carry semantic content (e.g., the "refer to the entire docuverse by '1'" usage at LM 4/28) — or would any single-component positive tumbler `[c]` with c ≥ 1 serve equivalently as the bootstrap root?

## Issue 7: P3 vs P3★ historical separation is unclear
Reason: Self-contained restructuring. The question is whether to tighten P3 to genuinely qualitative content or drop it entirely in favor of P3★; both options resolve from the ASN's own existing material.

## Issue 8: K.δ k=1 ghost-base discussion is excessively long and obscures the proof structure
Reason: Self-contained presentational tightening. All formal content is already present; the fix is to relocate implementation-evidence prose and meta-commentary while preserving the core precondition list and discharge mechanism.

## Issue 9: Worked examples are useful but their cross-referencing is fragmentary
Reason: Self-contained presentational fix. The coverage statement format already exists in the link-allocation example; the fix is to propagate it to other examples or add a coordinating table — no external content needed.
