# Review of ASN-0040

I worked through the proofs of B0/B0★, B1, B2, B4, B5/B5a, B6 (sufficiency and necessity), B7 (three cases), B8 (two cases), B9, B10, B_fin, and traced the worked example.

## Verification notes

- **B6 necessity case partition is exhaustive.** Sub-case (a) (defects in p's preserved prefix, including singleton [0]) versus sub-case (b) (pure trailing zero) covers all T4 violations of p; within (b), d = 1 routes to the B8-collapse argument via stream identity S(p, 1) = S(p', 2), d = 2 routes to TA5(d)-separator adjacency. Verified by enumerating T4(i)–(iv) failure combinations.
- **B7 case analysis exhausts the configuration space.** Different lengths (T3), equal lengths + non-nesting (T10), equal lengths + nesting (forced d = 2, d' = 1, divergence at #p+1). I checked the trace examples for Case 2 ([1,0,1] vs [1,0,2]) and Case 3 ([1] depth-2 vs [1,1] depth-1) and they exercise the proof branches correctly.
- **Stream identity argument.** c₁ = inc(p, 1) = [p₁..p_{#p-1}, 0, 1] and c'₁ = inc(p', 2) = [p₁..p_{#p-1}, 0, 1] agree component-by-component; the deterministic shared recurrence cₙ₊₁ = inc(cₙ, 0) extends this to full stream equality.
- **B8 same-namespace case correctly cites B0★.** The lift from a ∈ Σ₁'.B to a ∈ Σ₂.B uses multi-step monotonicity; B1 at Σ₂ then forces m₂ ≥ m₁+1, and S0 + T1 irreflexivity close the inequality.
- **Inductive dependency order is acyclic.** B_fin (from B₀ conf. + B0a) → B10 (from B_fin + B6 + TA5a) → B1 (from B10 + B0 + B7 + S0). Each inductive step uses earlier invariants at the IH state, no circularity.
- **Bridge1/Bridge2 cleanly bound to activation discipline.** The forward requirements are explicitly labelled as obligations on a future ASN; B₀ non-emptiness is sourced from Bridge2 composed with ASN-0034's allocated(s₀) = {t₀}, not slipped into B₀ conf.
- **Frame condition scope.** Bop is silent on non-Σ.B components, and the proofs in this ASN only manipulate Σ.B, so the partial specification does not undermine any internal claim.
- **Concrete coverage.** Steps 1–3, B7 Case 2 and Case 3 examples, and B9's M = 5 trace exercise the key postconditions against specific addresses.

## REVISE

None.

## OUT_OF_SCOPE

None.

VERDICT: CONVERGED
