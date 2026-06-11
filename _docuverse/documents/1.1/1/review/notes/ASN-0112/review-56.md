# Review of ASN-0112

I checked every derivation against the foundation contracts before rendering a verdict. Summary of what was verified:

- **Well-formedness of σ_d**: TS4 gives `origin_d < reach_d`; the divergence bound `k ≤ #origin_d` holds in both the equidepth (S8-depth) and cross-subspace (`k = 1`) cases; D0's preconditions are fully discharged, and its postconditions deliver exactly the Pos/actionPoint/T12 facts claimed.
- **V2's two covering cases**: case 1 correctly invokes D1 (all three preconditions present); case 2's componentwise computation through TumblerSub at `zpd = 1` and TumblerAdd at `k = 1` is correct — I recomputed it, including the proper-prefix conclusion `reach_d ≺ r⋆` via T1 case (ii). The depth-divergent variant (`extent_d = [1,2,0]`, `r⋆ = [2,2,0]`) checks out.
- **V5's exact cover**: the prefix-pinning step correctly excludes any depth-`m_s` tumbler diverging below the last position (both directions of T1 case (i) yield contradictions, and zero-component tumblers fall out the same way), and the boundary-cell step is a legitimate NAT-discrete application. The two-step structure honestly addresses what D-CTG★ is silent on.
- **V6's witness**: `w⋆ = [s_C,1,…,1,n_C+1]` satisfies `origin_d < w⋆ < reach_d` and `w⋆ ∉ O(d)`; the corollary's `origin_d.0` argument is correct (case (ii) then case (i) at position `m_s`).
- **V9a's inverse**: the discriminator `e_{#e} > 0 ⟺ #o ≤ #r` is proved in both directions (the `#o > #r` case correctly forces cross-subspace via S8-depth, hence `zpd = 1` and a zero-padded tail; the `#o ≤ #r` case is exhaustive over `zpd = #r` vs `zpd < #r`, with zero-freeness of `r` carrying the tail-copy positivity). Recovery of `r` and the final-component decrement (`r_{#r} ≥ 2`) are both sound. The biconditional in V9 assigns functionality and injectivity to the correct directions.
- **V12's count identity**: `extent_d = [0,…,0,n_s]` via TumblerSub at `zpd = m_s` is correct and matches both golden cases (`0.11` at n = 11; `0.3` in the worked report).
- **V18**: all six transition behaviors are individually discharged; the uniform fixed-origin argument genuinely covers each occupancy-preserving case rather than proving one and waving at the rest; the non-empty-preserving scope correctly excludes full clearance.
- **wp analysis**: both `Exact` and `Tight` are non-trivial, with exhaustiveness resting on S3★-aux as claimed.
- **Boundary cases**: empty document (V11, distinguished `⟨⟩`), link-only document (V5 link instance plus the content-clearing path in V18), all three depth orderings (`m_C <, =, > m_L`). The `n_s = 1` case is covered uniformly — no proof case-splits on it, so no separate treatment is owed.
- **Anti-bloat scan**: back-references dominate, with a single forward reference (V9 → V12); no deferral chains, no ordering justifications, no consumer inventories, no axiom-rationale prose. The V3 tightness appeal lands on a statement the TA5 foundation explicitly makes (least same-length successor when `sig(t) = #t`), and S8a's zero-freeness discharges its `sig(w) = #w` precondition here, so the citation is legitimate rather than a hand-wave.

## REVISE

No issues found.

## OUT_OF_SCOPE

### Topic 1: Exact per-subspace reporting for cross-subspace documents
**Why out of scope**: V6 proves the single span cannot trace a separated series; the two-span exact decomposition is explicitly assigned to RETRIEVEDOCVSPANSET (ASN-0113) in the scope list, and the ASN correctly stops at the bounding-box characterization.

### Topic 2: Extent-to-count relation in the multi-subspace case, and historical-version reporting
**Why out of scope**: Both are already recorded in the ASN's Open Questions; neither is a gap in the present operation's contract, which is fully specified for all reachable arrangements.

VERDICT: CONVERGED
