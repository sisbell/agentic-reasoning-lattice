Reading the foundation statements and the ASN as a system. The main analytical work is in D-CTG-depth (SharedPrefixReduction), which is the most structurally complex proof.

**D-CTG** is stated as an invariant with well-typed guards. The inner quantifier's conditions (`subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0`) jointly imply S8a when `#u ≥ 2` (which follows from `u ∈ V_1(d) ⊆ dom(Σ.M(d))` and S8a on that domain). D-CTG's depends list is coherent.

**D-CTG-depth first postcondition.** The contradiction argument is sound. The constructed `w` (with `wᵢ = uᵢ` for `1 ≤ i ≤ j`, `wⱼ₊₁ = n`, `wᵢ = 1` for `j+2 ≤ i ≤ m`) satisfies every D-CTG guard: `w ∈ T` by T0 comprehension; `subspace(w) = w₁ = u₁ = 1` because `j ≥ 2`; `#w = m = #u`; `zeros(w) = 0` because every component is ≥ 1 (copy from `u` satisfies S8a, `n > uⱼ₊₁ ≥ 1`, trailing `1`s); `u < w < x` via T1(i) at positions `j+1` and `j` respectively. T0(a) supplies arbitrarily many distinct values of `n`, yielding infinitely many distinct `w` in `V_1(d)`, contradicting S8-fin. The `j = m-1` edge case is handled correctly (the `wᵢ = 1` clause is empty; `wₘ = n` serves as the action-point component). ✓

**D-CTG-depth second postcondition (reduction step).** For any D-CTG-intermediate `v` satisfying the betweenness guard `u < v < x`, the proof shows `v` must share components `1..m-1` with `u` and `x` (contradiction via T1 trichotomy if not). With all three sharing that prefix, T1(i) reduces `u < v < x` to `uₘ < vₘ < xₘ`. The argument is valid. The extension to component 1 (subspace = 1 for all three) is clean.

**OrdShiftHom.** Part (a) uses `m ≥ 2` to place position 1 in the copy region (T1(i) action point = `m`, so prefix holds for `1 < m`). Part (b) correctly propagates S8a by using OrdinalShift's exported bound `shift(v,n)_{#v} = v_{#v} + n ≥ 1` for the action-point component. All preconditions to OrdinalShift, OrdinalDisplacement, TumblerAdd, and TA0 are discharged.

**S8a.** The two-step unfolding (`zeros(t)=0` → empty zero-set via NAT-card → all components positive via NAT-zero) is correctly cited and the chain is complete.

**Cross-claim consistency.** S8-depth is consumed by D-CTG-depth to obtain a common depth `m` across V_1(d). S8-fin provides the cardinality contradiction. No circular dependency is present: D-CTG-depth takes D-CTG as an axiom (invariant) and S8-depth as a design axiom; neither depends on D-CTG-depth. OrdShiftHom is cited only in S8-depth's narrative and is not invoked in D-CTG-depth's proof steps.

One observation:

### D-CTG-depth second postcondition has no formal formula

**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder, ASN-0034); D-CTG-depth first postcondition
**ASN**: D-CTG-depth (SharedPrefixReduction), Formal Contract, Postconditions — *"Contiguity of V_1(d) is determined by component m alone, structurally identical to the depth-2 case."*
**Issue**: The first postcondition carries a formal quantified formula; the second is stated only as prose. The proof establishes a precise structural fact: for any `u, x ∈ V_1(d)` with `u < x` and any `v ∈ T` satisfying D-CTG's guard between them, `u < v < x ⟺ uₘ < vₘ < xₘ`. A downstream dependant (D-SEQ) that needs to formally cite the reduction must reconstruct the formula rather than simply instantiating the postcondition.
**What needs resolving**: Add a formal formula alongside the prose, e.g. `(A u, x : u ∈ V_1(d) ∧ x ∈ V_1(d) ∧ u < x : (A v ∈ T : subspace(v) = 1 ∧ #v = m ∧ zeros(v) = 0 ∧ u < v < x : uₘ < vₘ < xₘ))`, so the reduction is citable without re-derivation.

VERDICT: OBSERVE