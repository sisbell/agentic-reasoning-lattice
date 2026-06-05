# Review of ASN-0113

I worked through the operation definition (W7/W8), the single-subspace extent machinery (W2–W5), the cross-member invariants (W9–W17), the weakest-precondition characterization (W20), and the four worked instances. I checked every proof against the foundation contracts it cites.

## Findings

The proofs hold up under scrutiny, including the places where this kind of note usually hand-waves:

- **W4 (ExactCoverage)** correctly invokes T5 on the shared prefix `[S,1,…,1]` of `start_S` and `reach`, and the aside that the lower bound *alone* cannot confine the prefix (the `[S,2,1] ≥ [S,1,1]` remark) is exactly right — the confinement is the joint effect of both bounds. Both inclusion directions are discharged.
- **W5 (ExactnessRequiresContiguity)** is the strongest part. The non-emptiness hypothesis is load-bearing and correctly excluded rather than swept in (the empty case has no min/max referent and is false on the left, since no span denotes ∅). The forward direction builds the span at the run's *actual* minimum rather than reusing W4's canonical anchor — and the `{[S,5,3],[S,5,4]}` counterexample shows why that distinction matters. The interior-divergence argument (T0(a) unboundedness + S8-fin finiteness forcing a shared prefix) and the order-convexity converse are both complete.
- **W10/W11** correctly avoid T7 (whose `zeros=3` precondition the denotation tumblers fail, per the `[S,1,0,1]` example) and rest disjointness solely on `t₁ = S` + SC-NEQ.
- **W12 (ProfileIrreducibility)** discharges reachability over *valid composites* with the full coupling discipline (J0 ∧ J1★ ∧ J1'★), correctly distinguishing the coupled K.α+K.μ⁺+K.ρ content composite from the uncoupled K.λ+K.μ⁺_L link composite, and spells out the symmetric witness rather than asserting "similarly."
- **W20 (ResultCardinalityWP)** correctly conjoins `d ∈ dom(M)` (since outside the domain the result is undefined, not `⟨⟩`) and the left-to-right weakest-precondition obligation is properly justified by W6/W7 totality.
- **Boundary coverage** is complete: unallocated `d` (W-pre), allocated-empty (W0), one-member (worked instance `d'`), degenerate `m_S=2`, and the depth-3 instance that exercises prefix-confinement where it is *non-vacuous*. The W-pre/W0 distinction (failure marker `?` vs. defined `⟨⟩`) is sharp and correctly maintained.

All references are to foundation ASNs (0034/0036/0047/0053/0093); no cross-ASN dependency on a non-foundation note, and `VSlice` is the only new notation, introduced cleanly. The implementation citations function as confirming evidence, not as the specification's content, so the note stays abstract — no drift.

## OUT_OF_SCOPE

The ASN correctly confines out-of-scope topics (single overall extent, version-fork permanence, transclusion, subspace extension) to its Open Questions rather than asserting claims about them — nothing to flag.

VERDICT: CONVERGED
