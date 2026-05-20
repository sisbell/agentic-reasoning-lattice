# Channel Assignment — ASN-0094 review-24

**Date:** 2026-05-20 04:25

## Issue 1: AllocatedAddressAntichain — no concrete example
Reason: The fix is to walk through the existing case analysis on concrete tumbler values. All needed structure (T4-validity, subspace partition, NAT-card enumeration) is already defined in the ASN; no design intent or implementation evidence is required.

## Issue 2: RetractionTargetNotOnChain — no concrete example
Reason: The fix is to exhibit the existing two-case proof on concrete `(b, d)` pairs. All cited primitives (NAT-card, T10a.7, T4b, L1, L1a, scaffolding clauses) are already in scope and the proof structure is fully specified internally.

## Issue 3: EffectiveWpSimplification — no concrete walkthrough
Reason: The fix is to trace the existing two-step discharge through concrete states already constructed in the Attributed Retraction walkthrough. Sh1/Sh3 and the RetractionTargetNotOnChain lemma are already established; the example just exhibits them.

## Issue 4: `latest_K_for_addr` empty-`S_d` path not exercised concretely
Reason: The fix is to add a brief subcase at `Σ_0` (already defined in the Coverage walkthrough as having `dom(Σ_0.L) = ∅`), showing `S_{d_subject} = ∅ ⟹ latest_K_for_addr = ⊥`. Pure exhibition of existing template semantics.

## Issue 5: Catalog-wide citation audit table omits the layer composite
Reason: Pure presentation/organization fix — either relocate the `K_is_fresh` row or add a header clarifying that it illustrates a failed check. No external input needed; the discipline criteria and exclusion rationale are already stated in the surrounding prose.

## Issue 6: Sh-conf's interaction with K.σ/K.α not explicitly scoped
Reason: The fix is a one-sentence clarification extending the existing "Sh-conf binds Emit_K, not K.λ" statement to mention K.σ and K.α. The Sh0–Sh3 Case A enumerations already establish that K.σ/K.α preserve `Σ.L`, so the scope claim is already implicit; only an explicit statement is needed.
