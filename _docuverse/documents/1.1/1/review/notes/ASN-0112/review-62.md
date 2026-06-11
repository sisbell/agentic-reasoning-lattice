# Review of ASN-0112

I worked through every derivation independently — the T12 legality argument, both covering cases of V2, the V5 prefix-pinning/discreteness argument, the V6 witness, the V9a inverse construction with its final-component discriminator, the V9b zpd case split, both wp derivations, and all four worked configurations (main, content-only, depth-divergent, mirror). The arithmetic checks out in every case I recomputed:

- **V2, cross-subspace case**: TumblerSub at `zpd = 1` gives `extent_d = [reach₁−origin₁, reach₂, …, reach_q, 0, …, 0]` of length `p`; TumblerAdd at action point 1 cancels in ℕ and copies the tail, yielding `r⋆` with `reach_d` as a proper prefix, hence `reach_d < r⋆` by T1 case (ii). Coverage holds in both depth regimes.
- **V5**: the two-step restriction argument correctly acknowledges that D-CTG★ is silent on the boundary cell and on non-slice tuples, and discharges both — prefix-pinning by T1 case (i) at the first divergence (covering zero components and wrong first components alike), boundary discreteness by the TA5 tightness established at V3. The `occupied-depth` definition is the right faithfulness notion, and the document honestly shows why bare strict inclusion cannot carry the V5/V6 dichotomy (the zero-extension `origin_d.0` witness).
- **V9a**: the discriminator `e_{#e} > 0 ⟺ #o ≤ #r` is correct in all three regimes (single-subspace: `e_{#r} = n_s > 0`; cross-subspace `m_C ≤ m_L`: tail copy positive by zero-freeness of `reach_d`; cross-subspace `m_C > m_L`: zero-padded tail). The reconstruction `r = [o₁+e₁, e₂, …, e_{sig(e)}]` verifies against the depth-divergent variant (`o = [1,1,1]`, `e = [1,2,0]`, `sig(e) = 2`, `r = [2,2]` ✓) and D1 closes the positive case (mirror: `[1,1] ⊕ [1,1,2] = [2,1,2]` ✓).
- **V9b**: single-subspace endpoints diverge exactly at `m_s ≥ 2` (S8a supplies the depth bound), zeroing slot 1; cross-subspace endpoints diverge at slot 1 with `s_L − s_C = 1`. The dichotomy aligns with V5/V6 via S3★-aux exhaustiveness, including the vacuous `⟨⟩` branch.
- **Quadrant analysis**: `(¬Tight, ¬LU)` impossibility is correct (`#o > #r` and `#o < #r` exclude each other), and the mirror variant correctly realizes the remaining `(Tight, ¬LU)` quadrant with both width discriminators reading correctly.
- **V18**: the two migration points are exhaustive over the non-empty-preserving editing vocabulary; the uniform fixing argument correctly routes through occupancy-status preservation, the m_S(d) re-pinning discipline, and D-MIN★ at both pre- and post-state. K.μ⁺_L's content-frame, occupancy-preserving K.μ⁻ on either subspace, and K.μ~'s domain preservation are each handled rather than waved at.

Foundation usage is consistent throughout: `sig(w) = #w` is correctly derived from S8a zero-freeness via TA5-SIG directly (not via TA5-SigValid, whose T4 precondition V-positions do not meet), D0/D1's preconditions are discharged before each invocation, and the TA6 sentinel reading of the implementation's zeros is correct. No foundation notation is reinvented; cross-references are confined to foundation ASNs.

On the anti-bloat axis: the prose is dense but load-bearing. The single Open Questions deferral at V3, the inline quadrant parenthetical in the mirror variant, and the abstract TS2/T3 recap in V9a each carry content rather than meta-justification. I found no relocated-finding residue, no use-site inventories, no ordering apologetics, and no duplicated paragraphs.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Failure protocol for an unallocated document identity
**Why out of scope**: The ASN fixes the precondition `d ∈ dom(M)` and correctly says nothing about what a conforming system returns when it is violated (error value, refusal, protocol response). That is operations-protocol territory for a future ASN, not a defect in the value semantics specified here.

### Topic 2: Extent-to-cardinality invariant in the cross-subspace regime
**Why out of scope**: The ASN proves the single-subspace count identity (V12) and explicitly opens the cross-subspace question (Open Question 1); relating a bounding-box extent to occupied counts across the inter-subspace void is new territory, likely interacting with per-subspace reporting.

### Topic 3: Historical-version report faithfulness
**Why out of scope**: What a span report over a designated past version must preserve relative to the present arrangement (Open Question 3) requires the version-graph machinery and belongs to a version-comparison ASN, not this boundary query.

META: (not applicable — the ASN specifies state-observing semantics, invariants, and discriminators abstractly; any conforming implementation must satisfy them.)

VERDICT: CONVERGED
