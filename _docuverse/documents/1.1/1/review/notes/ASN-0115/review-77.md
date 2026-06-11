# Review of ASN-0115

I worked through every lemma proof (Confinement, UnitSpec), every claim R0–R11 with its justification, all four worked instances against the foundation contracts, and the depth-compatibility override machinery. I also scanned specifically for the forward-reference accretion patterns flagged for this note. Findings below.

## Verification notes (what was checked and held)

- **Confinement lemma**: T5's preconditions are discharged exactly (`p ≼ s` and `p ≼ reach(σ)` via TumblerAdd's prefix-copy below the action point; `#p = m − 1 ≥ 1` from `m ≥ 2`). The `m = 2` boundary works (`p = [s₁]`).
- **Override soundness, deep case**: the two sub-cases (`m_S(d) < m − 1` against Confinement's length bound; `m_S(d) = m − 1` forcing `v = p ≺ s`, contradicting `v ≥ s` by T1 case (ii)) are each closed correctly — no hand-wave.
- **UnitSpec**: (a)–(d) each discharge their preconditions explicitly; the equal-length-prefix-is-equality step in (c) correctly chains Prefix, S8-depth, and T3. `zeros(d) = 2` is legitimately recovered from `dom(Σ.M) = E_doc` (M1) plus the Document predicate.
- **R6 gap analysis**: the bindable-slice characterisation is complete — Confinement excludes named positions shallower than `m_S` (the only depth-`(m−1)` candidate is `p`, which is below `s`), S8-depth excludes deeper bound positions, and D-SEQ★ makes the unbound slice members exactly the tail `k > n_S`. The `act = ∅ ∧ V_S(d) ≠ ∅` parenthetical covers a real case (span wholly past the frontier), not an excluded one. The worked instance's arithmetic checks out (slice cardinality 5, frontier 4, terminal overrun `{[1,5],[1,6]}`, attainment condition `2 + 5 − 1 = 6 > 4` consistent with non-attainment).
- **Nominal-extent corollary**: the biconditional is verified in all three branches, including the degenerate `act = ∅` sub-case of the third branch (full binding of the slice would force `slice ⊆ act`, contradiction).
- **R7**: the subtle dependence of `depthcompat` on `m_S(d)` — a whole-subspace quantity, not a property of the restriction — is correctly neutralised: a shared bound position pins `m_S(dⱼ) = #v` at both states when the restriction is non-empty, and both branches of `act` collapse to `∅` when it is empty. Link items need no store invariant (address-only payload); content items get S0 across `Σ →* Σ'` with store membership from S3★. The converse-failure remark (S4 value coincidence) is substantive, not padding.
- **R8**: the shared-subspace dispatch correctly routes through S3★-aux before applying the S3★/L14 contrapositive; the link-vacuity argument (CL-OWN forces `d = d'`, CL-UNIQ forces `v = v'`) is complete.
- **Boundary cases**: empty spec-set (`p = 0`), empty arrangement (`V_S(d) = ∅`), depth mismatch in both directions, subspace `S ∉ {s_C, s_L}`, deeper-than-slice tumblers in the denotation, and the document-allocation boundary are all addressed; zero-width spans are excluded by T12/`Pos(ℓ)` with `ℓ_{#ℓ} ≥ 1` derived from ActionPoint rather than assumed.
- **Cross-ASN references**: every citation resolves to a foundation ASN (0034, 0036, 0043, 0045, 0047, 0053, 0058, 0082, 0086, 0093); the SD citations now correctly target L14/ASN-0047.
- **Anti-bloat scan**: I checked each rationale paragraph against the drift patterns. The override-rationale paragraph carries a concrete failure mode (shallow-start vacuuming), the frame-limit notes (R2 channel disclaimer, R6 allocation boundary) are single sentences doing scoping work, and I found no duplicated paragraphs, no use-site inventories, no ordering justifications, and no case analysis of precondition-excluded scenarios.

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Semantics of a request naming an unallocated document
**Why out of scope**: The V-spec definition makes `d ∈ dom(Σ.M)` a precondition, and the ASN explicitly marks this boundary ("R6 concerns the absence of *binding* … not the allocation of the document itself"). Whether such a request fails, is filtered per-spec, or is rejected whole is a failure-semantics question the ASN's own Open Questions already pose; it is new territory, not an error here.

### Topic 2: Boundary-straddling spans delivering mixed-kind items from one contiguous range
**Why out of scope**: The ASN deliberately excludes non-ordinal-level spans (with a concrete straddling counterexample) and routes both-subspace designation through spec-set composition. The straddling-span semantics is correctly deferred to its own Open Question.

### Topic 3: Channel-level faithfulness
**Why out of scope**: R2 is explicitly scoped to the denotation of `deliver`; transmission guarantees are disclaimed per Nelson 5/18 and listed as an Open Question.

VERDICT: CONVERGED
