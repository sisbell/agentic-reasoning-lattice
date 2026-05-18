# Channel Assignment — ASN-0047 review-100

**Date:** 2026-05-18 02:32

## Issue 1: K.α and K.μ⁺ split-definition pattern obscures the actual contracts
Reason: Purely structural — the fix is a presentational reorganization (either inline the amendments at the original definitions with a forward-pointer to the link-store introduction, or add symmetric amendment blocks for every amended transition). No external evidence about design intent or implementation needed.

## Issue 2: L3 narrative claims an implicit Θ ≠ ∅ that conflicts with the foundation Link definition
Reason: Consistency fix between L3's narrative and K.λ's explicit precondition. The ASN either narrows Link locally (and removes the redundant K.λ conjunct) or keeps the explicit conjunct (and removes the "implicit" claim). Both options are derivable from the ASN's existing content; ASN-0043's Link definition is already known.

## Issue 3: Atomic-vs-composite framework and notation collision underspecified
Reason: Notational/expository disambiguation. The ASN already contains the components (SequentialTransitionAxiom, ValidComposite★, intermediate-state language); the fix is to make the elementary/composite scoping of `Σ → Σ'` explicit in one paragraph. Derivable internally.

## Issue 4: K.μ~ "canonical expansion" status unclear — is it the only valid decomposition?
Reason: Definitional stipulation. K.μ~ is a *named composite* — what its name covers is a choice the ASN makes. Both readings (canonical-only vs. any-valid-decomposition) are internally coherent; the ASN selects and states one.

## Issue 5: K.μ⁻ "Admissible removal pattern" precondition is verbose and entangles three separate concerns
Reason: Purely expository — splitting a dense paragraph into numbered clauses matching the exhaustiveness lemma's structure. The content is already correct; only the presentation needs restructuring.

## Issue 6: L1c "T10a-conforming chain" terminology overstates the property
Reason: Terminological clarification of the ASN's own use of T10a from ASN-0034. The formal step-rule conformance vs. activated-allocator-tracking distinction is derivable from ASN-0034's T10a definition; the ASN can rename or scope-narrow without external input.

## Issue 7: K.μ⁻ amendment is supplied implicitly via D-CTG★/D-MIN★ supersession
Reason: Symmetric to Issue 1 — add an explicit "K.μ⁻ amendment" subsection paralleling the K.α and K.μ⁺ amendments. Pure structural fix; no external evidence needed.

## Issue 8: Worked example "interior content replacement" leaves J1★ vacuity for re-added addresses implicit at the suffix length
Reason: Pedagogical — write out the explicit sets `ran(M(d)|_{s_C})` pre- and post-composite to ground the range-based-at-composite-boundary semantics. The conclusion is already derived in the ASN's J1★/J1'★ definitions; the example just needs the computation shown.

## Issue 9: K.δ "freshness via T10a GlobalUniqueness" discharge implicitly relies on parent-allocator activation discipline not laid out
Reason: Activation discipline is derivable from ASN-0034's T10a (T2 spawn rule) applied at K.δ case (ii) operand `t`. The fix is to spell out the T2-spawn-step interpretation explicitly, or to add a parallel axiom. Both are internal authoring choices grounded in the foundation.

## Issue 10: "Cross-document disjointness chain" named as a lemma but no separate statement block
Reason: Pure formatting — promote the named lemma to a standalone block matching the K.μ⁻ exhaustiveness lemma's presentation. No content change needed.
