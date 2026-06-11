# Review of ASN-0115

## REVISE

### Issue 1: Worked instances assert exact deliveries from under-specified or unproven singleton active sets
**ASN-0115, §"What co-delivery does with transclusion" (R8 worked instance), §"coherent multi-origin assembly" (R9 worked instance), §"subspace crossing" (R10 worked instance), §"permanence of the source" (R11 worked instance)**: "`deliver(R, Σ) = ⟨⟨content, Σ.C(a)⟩, ⟨content, Σ.C(a)⟩⟩: two items…" (R8); "`act((d₁,σ₁),Σ) = {v₁}`" (R9); "`deliver(R, Σ) = ⟨⟨content, Σ.C(a_C)⟩, ⟨ref, a_L⟩⟩`" (R10); "`act((d', σ'), Σ')` takes its geometric branch and contains `v'` … and `deliver(R, Σ') = ⟨⟨content, Σ'.C(a)⟩⟩`" (R11).

**Problem**: All four instances rest on the fact that a spec "naming" a single bound position has active set exactly that singleton — and that fact is never established. Two distinct defects compound here:

1. *Under-specification (R8, R9, R10).* "Whose first spec names `w`" does not determine a span. Many ordinal spans have `w ∈ ⟦σ⟧`, and some of them also capture other bound positions — in the R8 instance, a span wide enough to cover both `u` and `w` "names `w`" yet yields a four-item delivery, falsifying the asserted two-item equality. As written, the asserted `deliver` equalities are not consequences of the stated hypotheses; they are true only for a particular span choice the instance never fixes.

2. *Missing exactness step (R11, and implicitly all four).* R11 does fix the span explicitly — `σ' = (v', δ(1, #v'))` — but then jumps from "`act` … contains `v'`" to a singleton delivery. Exact equality `act = {v'}` needs an argument: `⟦(v', δ(1, #v'))⟧ = {t : v' ≼ t}` (PrefixSpanCoverage, ASN-0043), and any bound `t ≽ v'` has `t₁ = v'₁`, hence lies in `V_{s_C}(d')`, hence has depth `m_{s_C}(d') = #v'` by S8-depth, hence equals `v'` by Prefix at equal length. None of these steps appears; the instance's conclusion `deliver(R, Σ') = ⟨⟨content, Σ'.C(a)⟩⟩` is asserted, not derived. The R6 instance shows the document's own standard — explicit span, explicit slice, explicit `act` computation — which the four later instances do not meet.

**Required**: State and prove a small unit-spec lemma once — for `d ∈ dom(Σ.M)` and bound `v ∈ dom(Σ.M(d))` with `subspace(v) = S ∈ {s_C, s_L}`: the spec `(d, (v, δ(1, #v)))` is well-formed (start inherits S8a from `v`; `δ(1, #v)` is level-uniform and ordinal-level), depth-compatible at `Σ` (`v ∈ V_S(d) ≠ ∅` pins `m_S(d) = #v` by S8-depth), and `act = {v}` (by PrefixSpanCoverage, Confinement/subspace agreement, S8-depth, and Prefix-at-equal-length). Then (a) rewrite the R8, R9, and R10 instances to build their specs explicitly as unit specs and cite the lemma, and (b) close the R11 instance's `act = {v'}` step by the same citation.

## OUT_OF_SCOPE

### Topic 1: Failure semantics for a spec naming an unallocated document
**Why out of scope**: The ASN makes `d ∈ dom(Σ.M)` a well-formedness precondition of the V-spec and explicitly delimits R6 to binding-absence within an allocated document; whether an ill-formed request fails wholly, partially, or is filtered is the territory of the open question "under what conditions may delivery fail outright" and of a future error-model ASN, not an error here. M1 (ArrangementMonotonicity) ensures a once-valid spec-set never loses this precondition, so the boundary is stable as drawn.

The remainder of the ASN holds up under scrutiny. The R6 moreover-clause now stated at depth `#s` is well-formed across both branches of `depthcompat`, and the bridge paragraph correctly discharges the `V_S(d) = ∅` branch vacuously and identifies the slices in the bound branch. The Confinement lemma's T5 application is sound (the `#p = m − 1 ≥ 1` precondition holds from `m ≥ 2`); the deep-case override argument's two sub-cases (`m_S(d) < m − 1` vs `m_S(d) = m − 1`) are exhaustive and each contradiction is correctly closed. R7's proof handles the one subtle dependency I probed hardest — that `depthcompat` consults `V_S(d)` and `m_S(d)` *beyond* the restriction `Σ.M(dⱼ)|⟦σⱼ⟧` named in the hypothesis — by pinning `m_S(dⱼ)` through a shared bound position in the non-empty case and routing both branches to `∅` in the empty case. R8's link-vacuity is exhaustive over the `d ≠ d'` (CL-OWN) and `d = d', v ≠ v'` (CL-UNIQ) splits.

VERDICT: REVISE
