# Review of ASN-0115

I read this as a question of whether `deliver(R, Σ)` is well-defined and whether R1–R11 are actually established — not merely asserted. I checked the Confinement lemma, the `act` override logic, the `item` totality argument, every claim's proof, and all five worked instances against the foundations. The note holds up.

## What I verified

**Confinement lemma.** Sound. `p ≼ s` and `p ≼ reach(σ)` (TumblerAdd copies the prefix below the action point), `s ≤ t ≤ reach(σ)`, T5 yields `p ≼ t`. The `#p = m−1 ≥ 1` precondition of T5 holds since `m ≥ 2`. The generalization past ASN-0058's C0a (dropping the binding/well-formedness precondition) is genuinely needed for the unbound-span case R6 analyzes, so this is extension, not reinvention.

**The `act` override.** The "bites only shallow" argument is correct: a bound `v ∈ dom(Σ.M(d)) ∩ ⟦σ⟧` forces `v ∈ V_S(d)` (Confinement), `#v = m_S(d)` (S8-depth), and `#v ≥ #s − 1` (Confinement prefix), so `#s ≤ m_S(d)+1`; the deep case collapses to `#s = m_S(d)+1`, where `v = p ≺ s` contradicts `v ∈ ⟦σ⟧`. Hence the deep geometric intersection is empty and force-empty discards nothing there. `depthcompat` is well-guarded (the disjunction shields `m_S(d)`). The motivating example (`m_S=3`, `[S,1]` vacuums vs `[S,2]` captures nothing) checks out.

**`item` totality** follows from `act ⊆ dom(Σ.M(d))` + S3★-aux; the subspace-3+ start case is correctly shown harmless (`V_S(d)=∅`, `act=∅`).

**R6 no-interior-hole.** All `act` cases covered (depth-incompatible → ∅; `V_S(d)=∅` → ∅; substantive → canonical start `[S,1,…,1,s_{m_S}]` with unbound tail `k > n_S` a terminal overrun; the `act=∅`/`V_S≠∅` parenthetical). The restriction to the bindable slice, and the explicit acknowledgment that deeper named positions are merely unbound (no T1-claim made), is exactly right.

**R7 repeatability.** The non-trivial step — that `depthcompat` agrees despite reading beyond the `⟦σⱼ⟧` restriction — is correctly carried by the shared bound position pinning `m_S` at both states via S8-depth. The link/content payload split (link item carries `a`, needs no store invariant; content item needs S0 across `Σ →* Σ'`) is sound, and the comparability hypothesis is correctly motivated by the possibility of divergent-branch value divergence under the allocation discipline.

**R8** link vacuity (CL-OWN forces `d=d'`, CL-UNIQ forces `v=v'`) and the content/link subspace dispatch (S3★ contrapositive + SD + S3★-aux) are both rigorous; the "one position named twice ≠ transclusion" distinction is handled. **R9** kind-asymmetry, **R10** crossing, **R11** wp + orphan instance all derive cleanly. S7(c), the R6 arithmetic (`[1,2]⊕[0,5]=[1,7]`, `act={[1,2],[1,3],[1,4]}`), and the R11 ordinal-level span `σ'=(v', δ(1,#v'))` all verify.

No proof-by-checkmark, no "by similarly," foundation citations correct, no non-foundation cross-ASN references, the empty-spec-set and unbound-span boundaries are settled, and the out-of-scope operations (link-structure reading, extent reporting) are deferred without smuggling claims.

On the anti-bloat dimension: the note is prose-dense, but the candidate blocks I examined are protected content — the `act` force-empty rationale carries a load-bearing emptiness proof plus a concrete example; the R2 "frame limit" and the R6 "boundary not covered" lines are does/does-not statements; the R7 comparability justification motivates a necessary hypothesis rather than imagining an excluded case. None of the listed accretion patterns (axiom-rationale sub-paragraphs, use-site inventories, repeated downstream deferrals, ordering justifications, duplicated paragraphs) fire cleanly. I will not manufacture a finding against the guidance's warning on false positives.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the Open Questions correctly route inline provenance, failure modes, dangling references, channel faithfulness, and straddling spans to future ASNs.)

VERDICT: CONVERGED
