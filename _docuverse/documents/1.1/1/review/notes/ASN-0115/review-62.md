# Review of ASN-0115

I checked this ASN as a content-delivery query specification: the `act`/`item`/`deliver` definitions, the Confinement lemma, and the proofs of R1–R11, with particular attention to the load-bearing constructs (the depth-compatibility override, R6's no-interior-hole argument, R7's cross-state repeatability, R8's transclusion analysis, and R11's weakest precondition). I traced every foundation citation to the claim statements supplied.

What I verified holds up:

- **Confinement lemma.** The `p ≼ s`, `p ≼ reach(σ)`, `s ≤ t ≤ reach(σ)`, then-T5 chain is correct; `#p = m−1 ≥ 1` is discharged by `#s ≥ 2`. The straddling counterexample (`s=[1,5]`, `ℓ=[2,0]`) is arithmetically correct and is genuinely non-ordinal-level, so it motivates the discipline rather than contradicting the lemma.
- **`act` override.** The force-empty branch is well-formed (the disjunction guards `m_S(d)`), and the two rationale claims check out: the discontinuity example (`m_S(d)=3`, shallow start `[S,1]` vacuums the subspace while `[S,2]` captures nothing) is correct, and the deep case `#s > m_S(d)` provably forces `dom(Σ.M(d)) ∩ ⟦σ⟧ = ∅` (a candidate `v` would be a proper prefix of `s`, hence `< s`), so the override truly changes nothing there. `item` is total on `act` via S3★-aux. Specs rooted in `S ∉ {s_C,s_L}` resolve to `∅` without ill-definedness.
- **R6.** The canonical-start derivation (`act ≠ ∅` forces `s = [S,1,…,1,s_{m_S}]`) correctly pins the bindable slice to vary only in the last coordinate, so unbound members are exactly the `k > n_S` tail. The disclaimer "a claim about the bindable slice, not about every named tumbler" is precisely calibrated: deep unbound positions (e.g. `[S,1,…,1,s_{m_S},x]`) *can* fall T1-interior to the active range, but R6 explicitly does not claim otherwise, and they are dropped from `act` so the delivered sequence stays gap-free. The `act = ∅ ∧ V_S(d) ≠ ∅` parenthetical correctly closes the remaining sub-case.
- **R7.** The hypothesis correctly requires comparability (`Σ →* Σ'`), not mere co-reachability — and this is necessary, since divergent K.α branches can store distinct values at the same fresh address. The active-set agreement argument is robust even to intervening clear/re-pin (a position bound at both states pins `m_S(dⱼ)` equal at both), and the link-vs-content split correctly invokes S0 only for content values while reference items need no store invariant.
- **R8.** The subspace-sharing proof (S3★ + SD + S3★-aux dispatch) is valid, and the link-vacuity argument (CL-OWN forces `d=d'`, then CL-UNIQ forces `v=v'`) correctly confines genuine transclusion to content. "Byte-indistinguishable from coincidental value-equality (S4)" is sound given S4 permits distinct addresses with equal values.
- **R11.** Condition (i) is genuinely the weakest precondition for "delivery sources the value at `a`," and the decomposition (S3★ supplying membership, S0 supplying permanence as automatic consequences) is correctly framed. The orphaned-content worked instance is realizable (the K.μ⁻ contraction removing `v_d`'s binding can be taken as `n'_{s_C}=0` on `d`, leaving `d'` untouched by frame).

Foundation citations (S3★, S3★-aux, CL-OWN, CL-UNIQ, SD, S0, S8-depth, D-SEQ★, S4/S5/S7, T5, TumblerAdd, m_S(d)) match the supplied statements; the Confinement lemma legitimately generalizes ASN-0058's C0a (which is narrower, content-references-only) by re-proving from T5/TumblerAdd rather than restating it. The new symbols (`act`, `item`, `deliver`, `depthcompat`) are RETRIEVEV-specific, not reinventions of foundation notation.

On the anti-bloat axis: I watched for forward-reference accretion (deferral chains, document-ordering justifications, "why-the-axiom" sub-paragraphs, use-site inventories, twin paragraphs). I found none — the Nelson/Gregory grounding is design-intent evidence in the corpus idiom, the `act`-rationale paragraph carries a load-bearing concrete example plus the deep-case no-op fact, and the recurring content-value/link-address asymmetry is applied to distinct ends in R1/R8/R9/R10 rather than restated. The prose was load-bearing throughout; I did not have to skip past meta-prose to follow any claim.

## REVISE

None.

## OUT_OF_SCOPE

### The Open Questions are appropriate deferrals, not gaps
**Why out of scope**: Inline provenance in the payload, permitted outright-failure conditions, dangling references under relaxed S3★, delivery-channel faithfulness, and single-span subspace-boundary straddling are all correctly deferred. The boundary-straddling case in particular is explicitly excluded by the ordinal-level discipline (Confinement), with the multi-subspace need served by *composing* per-subspace specs into the spec-set (R10) — so its absence is a designed scope boundary, not an omission in this ASN.

VERDICT: CONVERGED
