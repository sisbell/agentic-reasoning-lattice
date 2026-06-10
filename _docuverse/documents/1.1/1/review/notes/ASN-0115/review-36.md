# Review of ASN-0115

I read this as a specification of a pure query — resolution followed by faithful dereference — and checked each claim's proof, its boundary behavior, and its cross-references. The load-bearing arguments hold up. Below I record what I verified and why I found no revision items.

## REVISE

(none)

I traced every proof and boundary case:

- **Confinement lemma.** The TumblerAdd computation `s ⊕ ℓ = [s₁,…,s_{m−1}, s_m+ℓ_m]` (ordinal-level `actionPoint(ℓ)=m`) gives `p = [s₁,…,s_{m−1}] ≼ s` and `p ≼ reach(σ)`; T5 over `s ≤ t ≤ reach(σ)` yields `p ≼ t`. The `#p = m−1 ≥ 1` precondition of T5 is met since `m ≥ 2`. Sound, and the straddling counterexample (`s=[1,5]`, `ℓ=[2,0]`, `[2,3]∈⟦σ⟧` with subspace 2) correctly motivates the ordinal-level requirement.

- **R6 (gap filtering) — the original contribution.** The three-case split is exhaustive and each case is correct: (a) `V_S(d)=∅` is vacuous; (b) `V_S(d)≠∅, act≠∅` derives the canonical start `s=[S,1,…,1,s_{m_S}]` from a witness `v∈act` via D-SEQ★ + Confinement, then `bound ⟺ k≤n_S` gives a contiguous terminal overrun with no interior hole; (c) `V_S(d)≠∅, act=∅` is handled by slice/`V_S(d)` disjointness without needing the canonical form. The claim is honestly scoped to the bindable (depth-`m_S`) slice, and deeper named tumblers (e.g. `[1,2,1]` in the worked instance) are correctly classed as simply unbound-and-dropped rather than holes — no overclaim. The worked instance (`s=[1,2]`, `ℓ=[0,5]`, `reach=[1,7]`, `act={[1,2],[1,3],[1,4]}`, gap `[1,5],[1,6]`) checks out against R1/R3/R5/R6.

- **R7 (repeatability).** The asymmetry is correctly identified: link items (`⟨ref,a⟩`) are stable from resolution agreement alone, while content items need S0 across `Σ →* Σ'`. The insistence on comparability (not merely a shared ancestor) is genuinely necessary — two divergent branches can run the same K.α event (same deterministic address) with different values, so a shared resolved address could carry differing content while arrangement restrictions agree. The WLOG is justified by symmetry of value-equality.

- **R8 (transclusion).** The subspace-agreement step (S3★-aux to get `subspace(v)∈{s_C,s_L}`, then contrapositive of S3★ against SD) and the link-vacuity proof (CL-OWN forces `d=d'`, then CL-UNIQ forces `v=v'`) are both correct. The distinction between genuine transclusion (two distinct content positions) and one link position named twice is drawn cleanly. The within-document transclusion worked instance is reachable (S5, K.μ⁺).

- **R11 (permanent sourcing).** The wp decomposition into one live condition (i) plus the automatic consequence `a∈dom(Σ.C)` (S3★) + immutability (S0) is a real, non-trivial wp analysis, and the orphaned-but-referenced worked instance (contract `d` via K.μ⁻, deliver through surviving version `d'`) correctly exercises the K.μ⁻ frame.

- **Cross-references.** Every numbered citation in the body is to a foundation ASN (0034, 0036, 0043, 0045, 0047, 0053, 0058, 0082, 0086, 0093). Span-taking commands are named, not numbered. `m_S(d)` is used per ASN-0047 and grounded in S8-depth, not reinvented. R10 explicitly stops at delivering the link *address* and disclaims endset structure (ASN-0111 territory) — no scope overreach.

On the anti-bloat pass: R6/R9/depth-compat were tightened in the recent commits, and the remaining density (notably R8) is claim-then-justification where the box states guarantees and the prose proves them by *complementary* arguments (output-level value-only payload vs. computation-level independent resolution), not duplication. The bulk of the elaboration consists of statements of what RETRIEVEV does and does not do, which the directive exempts. I found no passage I had to skip to follow a claim.

## OUT_OF_SCOPE

### The five Open Questions are correctly deferred, not gaps
Straddling spans, outright-failure semantics, dangling references (resolved address with no entity), inline-vs-query provenance, and transmission-channel faithfulness are each genuinely new territory and are flagged as Open Questions rather than silently omitted. The ordinal-level V-spec precondition cleanly excludes straddling from this ASN; failure semantics is excluded by treating `deliver` as a function on well-formed spec-sets (`dⱼ ∈ dom(Σ.M)`). These belong to future ASNs.

VERDICT: CONVERGED
