# Review of ASN-0115

The core of this ASN is sound. The `act`/`item`/`deliver` definitions are well-formed and total on their stated domains; the Confinement lemma's T5 argument is correct (and its counterexample `s = [1,5]`, `ℓ = [2,0]` checks out); UnitSpec discharges all four parts with the right citations; the deep-case emptiness argument under the override is complete (both sub-cases `m_S(d) < m−1` and `m_S(d) = m−1` are closed); the R6 frontier analysis correctly derives the canonical start from `act ≠ ∅` and handles the `act = ∅`, `V_S(d) = ∅`, and depth-incompatible branches; R8's link-vacuity via CL-OWN + CL-UNIQ and the subspace-agreement dispatch via S3★/S3★-aux/SD are exact; and the five worked instances genuinely verify the claims they cite (the R6 instance's arithmetic — slice `{[1,2]..[1,6]}`, `act = {[1,2],[1,3],[1,4]}` — is correct). Three issues remain.

## REVISE

### Issue 1: R7 invokes `deliver(R, Σ')` without discharging its definedness precondition

**ASN-0115, §Repeatability (R7)**: "Let `Σ`, `Σ'` be two states … without loss of generality `Σ →* Σ'` … for which the consulted arrangement restrictions agree, `Σ.M(dⱼ)|⟦σⱼ⟧ = Σ'.M(dⱼ)|⟦σⱼ⟧` for every `j`. Then `deliver(R, Σ) = deliver(R, Σ')`."

**Problem**: V-spec-hood is state-relative by this ASN's own definition — `d ∈ dom(Σ.M)` is a conjunct of being a V-spec. The R7 hypothesis writes `Σ'.M(dⱼ)` and the conclusion applies `deliver(R, ·)` at `Σ'`, both of which presuppose `dⱼ ∈ dom(Σ'.M)`, but neither the statement nor the proof establishes it. The discharge is available and one line: M1 (ArrangementMonotonicity, ASN-0047/0093) gives `dom(Σ.M) ⊆ dom(Σ'.M)` along `Σ →* Σ'`. The statement also leaves unsaid at which state `R` is assumed to be a spec-set, which matters for the WLOG: if the given direction is `Σ' →* Σ`, the lift runs the other way.

**Required**: State that `R` is a spec-set at the earlier state of the pair, and cite M1 to lift each `dⱼ ∈ dom(M)` to the descendant state, so that the restriction equality and `deliver(R, Σ')` are well-defined in both WLOG directions. This ASN's foundation discharges comparable one-line obligations explicitly (cf. the per-step citation discipline of ASN-0034); R7 should not be the exception.

### Issue 2: the "nominal extent" sentence in §Exactness is incorrect as written

**ASN-0115, §Exactness and arrangement-relativity**: "the delivered quantity equals `|act(ρ, Σ)|`, the number of *active* positions, which equals the nominal extent only when the spec is depth-compatible and no position in the interval is unbound."

**Problem**: Two defects. First, "nominal extent" is undefined — and it cannot mean `|⟦σ⟧|`, which is infinite (every extension of a member is a member). The intended reading must be the width's deepest component `ℓ_{#ℓ}`, the cardinality of the bindable slice. Second, "no position in the interval is unbound" is unsatisfiable under the ASN's own usage of "named position": the R6 analysis itself states that "named positions of `⟦σ⟧` deeper than `m_S` are necessarily unbound," and the ASN's own worked instance exhibits `[1,2,1] ∈ ⟦σ⟧` unbound. Read literally, the "only when" clause therefore asserts the equality *never* holds — yet it plainly can (take the R6 instance with `s = [1,1]`, `ℓ = [0,4]`: `|act| = 4 = ℓ₂`). A necessary-condition claim whose condition is vacuously false is wrong, not merely loose.

**Required**: Define the nominal extent as `ℓ_{#ℓ}` (equivalently, the cardinality of the depth-`#s`, subspace-`S` slice of `⟦σ⟧`), and restrict the unboundness condition to that slice: `|act(ρ, Σ)| = ℓ_{#ℓ}` iff the spec is depth-compatible and every member of the bindable slice is bound (`s_{#s} + ℓ_{#ℓ} − 1 ≤ n_S` under the canonical start). Both directions then hold by the R6 frontier analysis.

### Issue 3: duplicated formulation-justification prose around R6 (forward-reference accretion)

**ASN-0115, §Partial delivery, paragraph immediately after the R6 box**: "The bindable slice is stated at the span's own depth `#s` so that the moreover-clause is well-formed on the whole of `depthcompat`'s domain: … in the only depth-compatible branch with bound positions, `V_S(d) ≠ ∅`, depth compatibility forces `#s = m_S(d)`, so the depth-`#s` slice coincides with the depth-`m_S` slice the analysis below works in."

**Problem**: This paragraph is a defensive justification of phrasing rather than an advance of the argument, and its content is restated twice more in the same section: "Otherwise `V_S(d) ≠ ∅` and `#s = m_S(d)` — the span is rooted at exactly the subspace's common depth `m_S`," and again "in this branch `#s = m_S(d)`, so this is exactly the claim statement's depth-`#s` slice." Its vacuous-branch reading (`V_S(d) = ∅`: slice never meets the empty active range) also duplicates the analysis's own `V_S(d) = ∅` case, which derives the same conclusion properly via Confinement. The same point made three times is exactly the accretion pattern this note is flagged for.

**Required**: Keep the one fact the paragraph uniquely carries — `m_S(d)` is undefined in the `V_S(d) = ∅` branch while `#s` is not, which is why the slice is pinned at depth `#s` — as a single parenthetical (in the R6 box or at the head of the case analysis), and delete the rest of the paragraph along with the redundant slice-coincidence restatement inside the bindable-slice sentence.

## OUT_OF_SCOPE

### Topic 1: (none beyond the ASN's own Open Questions)
**Why out of scope**: The genuine extensions — straddling spans, transmission-channel faithfulness, failure-instead-of-partial-delivery semantics, dangling references under a relaxed S3★, inline provenance — are already correctly identified and deferred in the ASN's Open Questions section; none of them is an error here.

VERDICT: REVISE
