# Channel Assignment — ASN-0102 review-4

**Date:** 2026-05-28 14:43

## Issue 1: Source references not pinned to the content subspace
Reason: The mechanical fix (add a `subspace(u_i) = s_C` conjunct to P1) is internal, but whether COPY is *meant* to forbid link-subspace sources — rather than route them through S3★'s `s_L` branch — is a design-intent question (Nelson) that the implementation can corroborate (Gregory).
Nelson question: Were inclusions / virtual copies intended to transclude content spans only, or was copying a link-subspace span ever an intended COPY input?
Gregory question: Does `docopy` (via `specset2ispanset` / `insertspanf`) accept source spans drawn from the link subspace, or does it restrict resolved source spans to content?

## Issue 2: Dangling references to claims not present in the note
Reason: Purely editorial — restate X12 and the J1'★ analysis affirmatively from material already in the note (both boundaries independent; `New`/`Old` split). No design intent or implementation evidence is required.

## Issue 3: Per-state invariant preservation for the new elementary transition is only partially discharged
Reason: Derivable from the ASN's own frame and ASN-0047's invariant set — links/entities untouched makes the L-/CL-/P8-/NodeLineage conjuncts vacuous, and P7/P4★ are discharged directly from `a_j+i ∈ dom(Σ.C)` (X3/C1) and the explicit `Σ.R` extension already in the Definition.
