# Review of ASN-0053

I checked every proof (WF, WR, S0–S11d), re-ran all eleven worked examples arithmetically, verified the SC exhaustiveness branching, and confirmed the foundation citations all target ASN-0034 (a listed foundation, so permitted).

## REVISE

None. The proofs discharge their preconditions explicitly where it matters (S5's TA-assoc/TA-LC chain, WR's D2 discharge, S11's containment-boundary derivation), the case analyses are complete, and the boundary conditions (empty difference, equal spans, adjacency-as-empty-intersection, single-span vs. two-span remainders) are each handled. Spot checks of the rigor I expected to be hand-waved held up:

- **SC exhaustiveness** — the four-boundary-point branching is genuinely exhaustive under the WLOG, including the start-equal/reach-unequal → containment routing.
- **S7's "exact representation fails"** — the infinitude argument (deeper zero-extensions s.0, s.0.0, … all lie in ⟦σ⟧ via T1 case (ii) then case (i), with T0(b) supplying infinitely many) is a real proof, not an assertion. This closes the covering-vs-exact question for the level-uniform regime.
- **S9 uniqueness** — all six divergence cases (1a/1b/2a/2b/3a/3b) are written out with their own chaining; no "by symmetry" left unshown except where the symmetric case is mechanically identical and the role-swap is stated.
- **S5 width composition** and **S4a/S3b inverses** — preconditions for the foundation lemmas are individually discharged.
- Every worked example's arithmetic (reaches, ⊖ at the divergence position, ⊕ round-trips) is correct.

The pervasive `level-uniform` + `level-compatible` restriction is honestly scoped: WF's counterexample ([1,5] ⊖ [1,3,5] = [0,2,0] ≠ [0,2]) shows why unequal length breaks the round-trip, and the unequal-length operations are deferred to the open questions rather than smuggled in.

I scanned specifically for the anti-bloat patterns (forward-reference accretion, relocated findings, axiom-rationale prose, duplicated paragraphs, consumer inventories). The SC per-case glosses and the trailing Nelson/Gregory confirmations are evidence-grounding and intuition, not meta-prose, and there are no "see below"/"deferred to" forward pointers in the body. Nothing here requires a precise reader to skip past noise to follow a claim.

## OUT_OF_SCOPE

### Topic 1: Intersection/difference/merge for unequal-length (non-level-uniform) spans
**Why out of scope**: Already deferred to the open questions ("Under what conditions does the intersection of two spans at different hierarchical levels admit a well-formed span representation?"). The level-uniform restriction is a deliberate scoping decision, not a gap in the present claims.

### Topic 2: Span-set difference bound (|normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|)
**Why out of scope**: The single-span difference bound (S11d, ≤2) is fully established; extension to span-set difference is correctly listed as a future open question.

VERDICT: CONVERGED
