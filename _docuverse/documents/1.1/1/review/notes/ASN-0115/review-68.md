# Review of ASN-0115

I reviewed this ASN as a content-delivery query specification, checking each of R0–R11, the Confinement lemma, the `act` definition machinery, and all five worked instances. Because the note carries the `review-mode.anti-bloat` classifier, I also scanned specifically for the flagged forward-reference and reviser-drift patterns.

## Verification performed (load-bearing claims)

- **Confinement lemma.** T5 application checks: `p = [s₁,…,s_{m−1}]` with `#p = m−1 ≥ 1` for `m ≥ 2`; `p ≼ s` and `p ≼ reach(σ)` (TumblerAdd copies the prefix below the action point `m`); `s ≤ t ≤ reach(σ)` yields `p ≼ t`. The conclusion correctly establishes `#t ≥ m−1` as a *consequence* of `p ≼ t`, so the agreement `tⱼ = sⱼ` for `j < m` is well-typed even for shallow `t`. Sound.
- **`act` deep-case argument.** The contradiction (`v ≼ s` proper ⟹ `v < s`, contradicting `v ≥ s`) correctly shows the geometric intersection is independently empty when `#s > m_S(d)`, so the override is conservative there. Sound.
- **R6 no-interior-hole.** The case split (depth-incompatible → `act = ∅`; depth-compatible with `V_S(d) = ∅` → `act = ∅`; depth-compatible at common depth) is exhaustive over the `act` definition. The canonical-start derivation `s = [S,1,…,1,s_{m_S}]` from a witness `v ∈ act`, the slice `{k : s_{m_S} ≤ k ≤ s_{m_S}+ℓ_{m_S}−1}`, and the bound condition `k ≤ n_S` (D-SEQ★) correctly force the gap to a contiguous terminal tail. The `act = ∅` sub-case (slice disjoint from `V_S(d)`) is handled. The qualifier restricting the guarantee to the bindable slice is honest. Sound.
- **R7 active-set agreement.** The non-empty-restriction case correctly pins `m_S(dⱼ) = #v` equally at both states from a shared witness (S8-depth); the empty-restriction case collapses `act` to `∅` at both regardless of branch. The link-item independence (carries address, no store invariant) versus content-item dependence (needs S0 along `Σ →* Σ'`) is correctly distinguished, and the comparability requirement (not merely shared-ancestor) is correctly justified — divergent executions can rebind a reused address to different values. The sufficiency-not-biconditional counterexample (S4 equal-value rebinding under contract+extend) is valid. Sound.
- **R8 link vacuity.** CL-OWN (`origin(a) = d` forces equal documents) composed with CL-UNIQ (link-subspace injectivity forces equal positions) correctly makes distinct link positions sharing an address impossible; both are in ExtendedReachableStateInvariants. The "shared subspace" step (S3★-aux to bound subspaces to `{s_C,s_L}`, then contrapositive of off-store S3★ plus SD) is complete. Sound.
- **R11 wp.** The single live condition (i) — an active content position resolving to `a` — is genuinely the weakest precondition; `a ∈ dom(Σ.C)` is its automatic, permanent consequence via S3★ + S0, correctly framed as a decomposition rather than a second conjunct. The fork-then-contract worked instance verifies `σ' = (v', δ(1,#v'))` is ordinal-level and depth-compatible, and the K.μ⁻ frame leaves `Σ.M(d')` intact. Sound.

All worked instances (R6 `s=[1,2]`, `ℓ=[0,5]`, `reach=[1,7]`; R8 reversed-order transclusion; R9 distinct-origin assembly; R10 mixed-subspace; R11 orphan-but-referenced) recompute correctly.

## REVISE

None.

## OUT_OF_SCOPE

None to add — the Open Questions section already enumerates the genuine future territory (inline provenance, failure-instead-of-partial-delivery, dangling references under relaxed S3★, channel faithfulness, boundary-straddling spans), and the ASN correctly defines no claims for the scoped-out sibling operations (RETRIEVEDOCVSPAN/SET, READLINK, FOLLOWLINK, etc.).

## Anti-bloat scan

I looked specifically for the flagged patterns and did not find them: no sub-paragraphs labeled "Scope"/"Why the axiom is needed"/"Protocol rationale"; no repeated downstream deferrals ("see X below," "deferred to Y"); no document-ordering justifications; no definitions enumerating downstream consumers. All ASN-NNNN references are to foundation ASNs (0034, 0036, 0043, 0045, 0047, 0053, 0058, 0082, 0086, 0093). The dense passages I scrutinized — the `act` discontinuity rationale, the deep-case conservativeness derivation, the R7 comparability justification — each carry a concrete example, a derived property, or a frame limit rather than skippable noise, so I am not manufacturing a weak finding against them. The Confinement lemma is reproved (a strict generalization of ASN-0058's C0a, dropping the arrangement-binding hypotheses) rather than bare-cited, which is appropriate.

VERDICT: CONVERGED
