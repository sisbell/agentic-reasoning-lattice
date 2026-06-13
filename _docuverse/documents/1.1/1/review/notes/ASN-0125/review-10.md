# Review of ASN-0125

This is a strong, carefully argued note. The central impossibility (EL0), the intent-invisibility theorem (EL1), the carrier-space elimination (EL2/EL3), and the two-step composite contracts (EL6/EL7) hold up under scrutiny; I checked the wp Case 2 invocations, the antichain/coverage arguments in EL4 and EL11(a), the commutativity proof in EL13, and the full worked example, and the formal content is sound. Two findings remain.

## REVISE

### Issue 1: Edit-discipline is never assembled into an invariant — the base case and Nullify/frame-op preservation are unstated
**ASN-0125, Df-DISC / EL6(v) / EL7(vi)**: Df-DISC says "A layer is edit-disciplined iff every state it reaches is," and EL6(v)/EL7(vi) prove "Σ₂ is edit-disciplined when Σ is" for assert_sup and editlink.

**Problem**: These preservation results are the *inductive step* of an invariant that is never assembled, so the entire conditional apparatus ("at disciplined Σ" — EL6iii, EL7iii, the EL7iv full-frame, EL14 active-at-birth) is left with no demonstrated, reachable, non-vacuous domain.
- **(a) No base case.** Σ₀ (ASN-0047, L₀ = ∅) has `S^{Σ₀} = ∅` and `L_R^{Σ₀} = ∅`, so it is vacuously edit-disciplined. This is exactly the empty-store boundary case the standards require, and it is the only thing that makes a disciplined state reachable from first principles. It is never stated.
- **(b) Nullify is not covered.** Nullify is one of the three declared layer operations, and the worked example uses it *inside* disciplined states (`Nullify(Σ, H, c₂)`, then further `assert_sup` whose "active at birth" depends on a disciplined pre-state). Yet the ASN never shows Nullify preserves edit-discipline.
- **(c) Frame-ops and the operation set are not pinned down.** The L-framing transitions (K.μ⁺, K.μ⁻, K.ρ, K.α, K.δ) and the original-link-creating bare K.λ are not addressed, and the admissible editing-layer operation set — which must *exclude* a bare non-conforming `Emit_{K_sup}`/`Emit_R` (EL1's Remark concedes the substrate cannot forbid these) — is never defined. The worked example's opening "The state is edit-disciplined" is therefore asserted, not derived.

**Required**: State the base case (Σ₀ vacuously edit-disciplined, L₀ = ∅). Observe that edit-discipline = ASN-0086's unit-depth retraction discipline ⊕ the claim schema, and discharge both halves for Nullify (adds a unit-depth [R] tuple, no [K_sup] claim) and for every L-framing transition (claims/retractions and `dom(L)` unchanged). Define the admissible editing-layer operation set so the maintenance invariant closes, giving the conditional claims a reachable domain.

### Issue 2: "Layer transfer" paragraph is a use-site inventory wrapped in a defensive disclaimer
**ASN-0125, "The substrate we build on" → "Layer transfer"**: "The ASN-0086 facts this note invokes — R0a (FlatLinkDomain), the emission-address function a_emit, the Emit/Observe/Nullify contracts, wp Case 2, R3 (TypedSliceMonotonicity), and R6a — each reference only the link store and the document set dom(M) ... We therefore use these particular facts at full-vocabulary reachable states ... — without claiming anything of ASN-0086 results this note does not use."

**Problem**: The transfer kernel — "ASN-0086's results depend only on Σ.L and dom(M); both evolve identically under ASN-0086's `{K.σ, K.α, K.λ}` and the full ASN-0047 vocabulary, so those results carry over" — is one sound idea. It is buried under (i) a use-site inventory of the six facts to be consumed downstream (the "enumerates downstream consumers" pattern), (ii) the defensive non-claim "without claiming anything of ASN-0086 results this note does not use," which asserts nothing, and (iii) the dangling referent "Both of those." This is precisely the accreted-meta-prose-around-forward-references pattern this review mode targets.

**Required**: Compress to the kernel — "ASN-0086's results depend only on Σ.L and dom(M); both evolve identically under the full vocabulary (Vocabulary fact V; M1), so those results hold at full-vocabulary reachable states" — and drop the fact inventory and the disclaimer.

## OUT_OF_SCOPE

(none) — The note stays on EDITLINK throughout. Reader-side queries (in/out, current, contextual/archival discovery) are intrinsic to specifying supersession recognizability, not general link discovery; genuinely new territory (meta-claim stratification, retraction authority, span-level correspondence, edit↔listing coupling) is correctly deferred to the Open Questions rather than half-built here.

VERDICT: REVISE
