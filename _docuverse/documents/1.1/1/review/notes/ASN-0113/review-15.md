# Review of ASN-0113

I checked every introduced claim (W0–W20) against its proof, with particular attention to the per-subspace coverage arguments (W4, W5), the disjointness/confinement chain (W9–W11), the profile-irreducibility construction (W12), and the weakest-precondition characterization (W20). I also re-verified the three worked instances and the foundation citations.

## REVISE

(none)

The proofs are complete and the boundary cases are handled explicitly:

- **W-pre / W0** correctly separate the three regimes — unallocated `d` (outside domain, fails), allocated-empty (`⟨⟩`), and populated — rather than collapsing "empty" into "absent."
- **W4** uses T5 with *both* bounds (the note that `start_S ≤ t` alone fails to confine the prefix is correct, and the lexicographic counterexample is apt). The pinning of the last component by the half-open bounds is sound.
- **W5** states the contiguity dependence as a biconditional with the non-emptiness hypothesis load-bearing and correctly excluded from the empty case (no span denotes ∅). The forward direction is built from the run's *actual* minimum (not the canonical anchor), and the T0(a)+S8-fin argument ruling out interior divergence is valid; the converse rests correctly on S0 order-convexity, with a concrete `{[S,1],[S,3]}` counterexample.
- **W10/W11** disjointness is grounded only on `t₁ = S` (W10) plus SC-NEQ, with an explicit and correct disclaimer that T7 is neither met nor needed (denotation tumblers may carry zeros).
- **W12** discharges reachability over genuine ValidComposite★ transitions, correctly distinguishing coupled `K.α+K.μ⁺+K.ρ` content composites (J0/J1★/J1'★ live) from uncoupled `K.λ+K.μ⁺_L` link composites (coupling vacuous, content-subspace-scoped).
- **W15** correctly observes that K.μ⁻ can contract both subspaces at once and that independence is a property of the disjoint counts, not of single-subspace transitions — a subtle point handled honestly rather than overclaimed.
- **W20** is a non-trivial wp partitioning allocated states by the two emptiness bits, with the left-to-right (weakest) obligation argued from totality of `occupied(d)`.
- The depth-3 worked instance specifically exercises the prefix-confinement step that is vacuous at `m_S = 2`, confirming W4 where it does real work.

Normalization (W13) correctly relies on N1/N2 from ASN-0053, which are pure order conditions and do not require the two differently-deep members to be mutually level-compatible.

## OUT_OF_SCOPE

The Open Questions appropriately defer version-fork permanence, transclusion-source editing, consistency with the single overall extent (ASN-0112), and subspace-list extension — all genuinely future territory, not gaps in this ASN. Open Question 2 (consumer reading "absent member" as "extent zero") is correctly flagged by W14 as a convention this note does not rely on.

VERDICT: CONVERGED
