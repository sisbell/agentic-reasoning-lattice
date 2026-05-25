# Channel Assignment — ASN-0098 review-6

**Date:** 2026-05-24 20:41

## Issue 1: Project function precondition absent from formal definition box
Reason: Pure formal-hygiene fix internal to the ASN — add the precondition `d ∈ dom(Σ.M)` to the definition box to match the style already used by `discoverable_from`. No design intent or implementation evidence needed; the convention is set by the ASN itself.

## Issue 2: LP10 boundary case — K.μ⁻ contracting to empty arrangement
Reason: The K.μ⁻ precondition admitting `n'_S = 0` is established in ASN-0047 and the projection-empty consequence follows mechanically from the projection definition. Adding an explicit boundary acknowledgment requires no external input.

## Issue 3: LP16 statement informally phrased
Reason: Formalization of an already-proved claim using vocabulary the ASN has fully established (`coverage`, `ran(Σ.M(d))`, `discoverable_from`). No design intent or implementation question is at stake — the proof already references the precise condition.

## Issue 4: LP19 multi-state chain obscures the lemma content
Reason: Presentation refactor of an existing proof. Whether to split into two lemmas or simplify the chain is an internal exposition choice; the content and proof obligations are already in the ASN.

## Issue 5: LP12 existential lift left implicit
Reason: Elementary proof completion using definitions (`discoverable_from`, `project`) already in the ASN. The lift from per-slot to existential biconditional is mechanical and requires no external evidence.
