# Review of ASN-0131

I checked every introduced claim against its body, verified the two RE-UDIST-∩ counterexamples for reachability and correctness, traced the RE-RET biconditional (both directions, with and without the `Θ`-hypothesis), recomputed the RE-CWP weakest precondition, and recomputed the worked instance's coverages and touch tests. I also confirmed the transition case analysis in the stability section is exhaustive over ASN-0047's vocabulary plus ASN-0082's shift primitives, and that every cross-reference is to a foundation ASN. The findings below are the verification results; no REVISE items survived.

Spot-verifications that held:
- **RE-ADDR** — the addressability argument is sound: `nullified` consults only `L_R^{Σ'}` (unit-depth Nullify outputs by the standing commitment), and R0a's antichain plus freshness (`ℓ_new ∉ dom(Σ.L)`) rules out every pre-existing covering retraction; the only self-cover is `ℓ_new` retracting its own emitter. "Retraction to-set in `Σ'.L`" correctly reads as `L_R`-membership, so higher-arity retraction-coverage links (which can carry wide to-sets) are irrelevant — they never enter `nullified`.
- **RE-UDIST-∩** — both counterexamples are reachable (non-injective `{[1,1]↦a,[1,2]↦a}` via M13/M14; injective `{[1,1]↦a,[1,2]↦b}` is the canonical arrangement) and both refute `⊇`; the split-witness obstruction in `touch_W` genuinely survives injectivity, so the "no arrangement restriction recovers `⊇`" diagnosis is correct. The touch-implication is verified as the exact iff.
- **RE-RET** — forward needs `coverage(Θ) ∩ dom(Σ.C) = ∅` only for the `i=3, e=Θ` self-retraction case (correctly scoped); backward needs only R-Scope + L12 + `M'=M` (correctly stated as hypothesis-free). The `ℓ₁`/`ℓ₂` worked illustration is consistent.
- **RE-CWP** — the `Δ = image ∖ I_R`, `I_R ⊆ image` decomposition and the `R=∅` collapse to `RE(W,d,Σ)=∅` are correct; "unchanged reduces to nothing-dropped" follows from the unconditional `⊆` direction.
- Worked instance — `a₂ ⊕ δ(2,#a₂) = shift(a₂,2) = a₄`, so the first span of `e₁` is `[a₂, a₄)` containing `a₂` and `a₃`, and every read-off (RE-OVL/CLIP/WHOLE/UNIT) is faithful.

The provisional status of RE-WHOLE is handled correctly: RE-CLIP is separated as the resolution-robust invariant, so downstream work has a stable foundation regardless of OQ1.

## REVISE

None.

## OUT_OF_SCOPE

### Topic 1: Grounding the conservative-lift assumption for shift-based insert/delete
**Why out of scope**: RE-EDIT's insert/delete stability rests on the *conservative-lift modelling assumption* — that ASN-0082's displacement primitives frame `Σ.L`, `Σ.E`, `Σ.R` when lifted from the `(C,M)` model to the full `(C,L,E,M,R)` state. The note adopts this honestly and hedges the claim accordingly, but the assumption is genuinely unprovable from the current foundation (ASN-0082 does not model the three extra stores). Establishing it belongs in a future ASN that extends the shift primitives to the full state, at which point RE-EDIT's insert/delete sub-claims become unconditional. This is the one dependency not already captured in the note's Open Questions list.

### Topic 2: The Open Questions 1, 4, 6, 7 already enumerated in the note
**Why out of scope**: The whole-vs-touching-spans choice (OQ1), the structurally-restricted sufficient condition for intersection-equality (OQ4), the type-slot-against-content match (OQ6), and the link-subspace region query `W ⊆ s_L` (OQ7) are correctly deferred. Each is new territory rather than a defect in the content-region operation this note specifies.

VERDICT: CONVERGED
