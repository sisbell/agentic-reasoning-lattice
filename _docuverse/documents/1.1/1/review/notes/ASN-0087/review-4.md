# Review of ASN-0087

I worked through the ASN against the foundation ASNs and verified each major proof and invariant claim.

## REVISE

(no items)

The ASN demonstrates rigorous engineering throughout:

- **Composite decomposition** is justified both structurally (forced order K.λ then K.μ⁺_L) and by reference to Nelson's design intent.
- **Precondition derivation** for `ℓ ∉ ran(Σ_mid.M(d))` correctly chains K.λ freshness through S3★ + S3★-aux + L14 to discharge K.μ⁺_L's first-arrangement requirement against pre-state quantities.
- **L1c chain derivation** is explicit per-step (d → b_C(d) → b_L(d) → t_1^L(d) → siblings), with TA5a admissibility bounds checked at each `k = 2` and `k = 1` step against the saturating zero count.
- **Freshness argument** is three-layered (within-chain via ChainEnumerationInjectivity; cross-subspace via DisjointSubAllocatorChains; cross-document via T10).
- **WP analysis** is non-trivial: home/non-home split, reflexive disjunct, and explicit collapse under standard authoring.
- **Σ_mid analysis** correctly establishes the intermediate state as fully reachable per SequentialTransitionAxiom, with all per-state invariants preserved, and characterises exactly when discoverability differs between Σ_mid and Σ'.
- **Side-effects on prior links** correctly invoke LP9 specialised to the single new V-position {v_ℓ ↦ ℓ}, and confine the window to the home document.
- **Worked example** verifies projection and discoverability against specific tumblers.
- **Invariant preservation** is stratified per-state / boundary / transition per ASN-0047 conventions; J0/J1★/J1'★ correctly identified as vacuous for link-subspace effects.
- **Reflexive endsets** explicitly disambiguated from the standard authoring path with reduction shown.

Boundary cases covered: first emission (V_{s_L}(d) = ∅), subsequent emission, N = 3 vs. N > 3, reflexive endsets, intermediate-state observability.

## OUT_OF_SCOPE

(no items — the Open Questions section correctly defers: endset well-formedness for endsets referencing not-yet-allocated addresses; protocol-layer composite atomicity; identity of MAKELINK invocations producing identical endset values; deferred-consistency models for discoverability; and resurrection semantics)

VERDICT: CONVERGED
