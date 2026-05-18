# Channel Assignment — ASN-0047 review-95

**Date:** 2026-05-17 23:52

## Issue 1: K.δ k=2 implicit constraint on operand level not stated
Reason: The constraint zeros(t) ≤ 1 is derivable from the K.δ precondition `¬IsElement(e)` combined with the case-(ii) k=2 structural identity `zeros(e) = zeros(t) + 1`. The fix is to make the implicit derivation explicit at the per-sub-case bullet — no external evidence needed.

## Issue 2: "Ghost-base versioning (k = 1)" paragraph is a pure pointer
Reason: This is purely editorial — the paragraph adds no content and merely points back to information already stated in the precondition list and Freshness discharge paragraph. Removal is internal.

## Issue 3: "Frame extension (existing transitions)" paragraph adds little
Reason: Editorial restructuring to absorb a structural-observation paragraph into the extended-state introduction or K.λ's frame statement. No external evidence needed.

## Issue 4: P3★ naming inconsistency — no P3 predecessor in this ASN
Reason: Naming convention choice — either rename to P3 (fresh synthesis) or introduce a four-component P3 predecessor. Internal to the ASN's own naming discipline; no external evidence needed.

## Issue 5: K.λ precondition collapses two discharge cases into one bullet
Reason: Editorial split of a precondition bullet for clarity. The two discharge routes and their predicates are already cataloged in the freshness-discharge summary table — formatting fix only.

## Issue 6: K.μ~ "full content-subspace clearance" presented as the decomposition rather than one decomposition
Reason: The math established in K.μ⁻'s exhaustiveness lemma and the worked example for interior replacement already shows partial-suffix decompositions are admissible. The fix is to acknowledge full clearance is one valid choice (chosen for uniformity) and that partial-suffix decompositions are admissible when π fixes a contiguous prefix. Derivable from existing ASN content.

## Issue 7: Bootstrap node value [1] presented as fixed without marking the conventional nature
Reason: Whether [1] is structurally privileged or one of many admissible single-component positive tumblers is a design-intent question — NodeLineage's `n₀ ≼ e` constraint is satisfied by any single positive tumbler, so the choice of [1] is not forced by the invariant.
Nelson question: Does Nelson's design require the bootstrap node address to be specifically `[1]`, or is it any single-component positive tumbler with `[1]` as the canonical convention consistent with the single root authority (LM 4/17–4/22)?

## Issue 8: SubAllocatorAxiom's necessity claim is incompletely justified
Reason: The reviewer's reconstruction of a multi-step T10a chain reaching [d.0.s_C.1] is a foundation-level claim about T10a's discipline (ASN-0034). The spec author can verify by examining T10a's actual per-(t, k') spawning constraints; either path (explicate the chain as abstraction, or identify the blocking T10a clause) is internal to the foundation content already referenced.

## Issue 9: Dual-phase (four-component → extended) structure produces cumulative amendment accretion
Reason: Structural presentation choice between single-phase and dual-phase exposition. The trade-off (pedagogical clarity of phases vs. accumulated amendment prose) is internal to the spec author's editorial judgment; no external evidence resolves it.

## Issue 10: J1 "derivation by wp" framing understates the design choice
Reason: Reframing the presentation to make P4 explicit as the design choice and J1 as the wp-induced coupling. The logical content is already correct — the fix is presentation order, internal to the ASN.

## Issue 11: K.δ structural identities could be presented as TA5-derived consequences
Reason: Marking which clauses are TA5/T4b-derived consequences vs. imposed preconditions. TA5 and T4b are referenced foundation content; the derivation is internal to existing reference material.
