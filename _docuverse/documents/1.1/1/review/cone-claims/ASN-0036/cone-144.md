## Audit

I read the full dependency cone — NAT-carrier through NAT-induction, Σ.M(d), T0, T1, subspace, V-sub, S8-depth, S8-fin, and D-MIN — as a system.

**NAT-* foundation layer.** The dependency graph is clean. NAT-carrier supplies ℕ as a set. NAT-zero adds 0. NAT-closure adds 1 and the addition map. NAT-order adds `<` and derives `≤` and ≤-transitivity. NAT-addcompat adds n < n+1 and right-order compatibility. NAT-discrete adds m < n ⟹ m+1 ≤ n. No circular dependencies; every symbol grounded at its defining claim.

**NAT-induction.** The axiom is minimal: NAT-carrier (for ℕ), NAT-zero (for 0), NAT-closure (for k+1 ∈ ℕ and 1 ∈ ℕ under the successor closure). NAT-order, NAT-discrete, NAT-addcompat, NAT-wellorder are all correctly absent — the prose argument that order-and-addition axioms do not entail induction is the known non-categoricity fact; the posit closes that gap without proof of the separating model.

**subspace.** The depth guard 1 ≤ #v places index 1 in T0's component-projection domain. T0's nonemptiness 1 ≤ #a discharges the guard universally, making subspace total on T. NAT-closure grounds the literal 1, NAT-order grounds the ≤; both are cited directly because T0 does not re-export them. Correct.

**Σ.M(d) and V-sub.** The partial-function typing T ⇀ T and the subspace-projection definition are clean definitional claims. V-sub's forward references (D-CTG, D-CTG-depth, D-MIN, D-SEQ) are accurate and these claims are not yet visible.

**S8-depth.** The axiom (A d,u,w : u ∈ dom ∧ w ∈ dom ∧ subspace(u)=subspace(w) : #u=#w) is a flat posit grounded at Σ.M(d) (for dom), subspace (for the guard), and T0 (for #·). S8a is correctly excluded: it contributes no symbol to #u=#w. OrdinalShift/OrdShiftHom are correctly classified as commentary citations, not dependency entries.

**S8-fin.** The bijection formulation of finiteness is correctly scoped to avoid the out-of-scope |·| operator. NAT-zero grounds n=0 at the base state (the unique admissible witness when AX-1 forces dom=∅). The four-way Depends list — NAT-carrier/zero/closure/order — all appear as first-class symbols in the formal axiom and are correctly traced. T0 supplies the tumbler carrier for the codomain typing; the segment notation's `1` and `≤` are grounded directly from NAT-closure and NAT-order rather than through T0.

**D-MIN — existence proof.** The least-index principle P(N) induction on N is correctly structured:

- *Base P(0)*: vacuously true — {j: 1 ≤ j ≤ 0} = ∅ carries no non-empty Q.
- *Step N → N+1*: the segment identity {j: 1 ≤ j ≤ N+1} = {j: 1 ≤ j ≤ N} ∪ {N+1} is proved in both directions. The ⊇ direction uses NAT-addcompat (N < N+1 to extend index bound) and the 1 ≤ N+1 chain (NAT-zero's 0 ≤ N → NAT-addcompat right-compat → NAT-closure identity → 1 ≤ N+1). The ⊆ direction uses NAT-discrete (m < n ⟹ m+1 ≤ n) plus NAT-order's irreflexivity and totality to show j ∉ {N+1} ∧ 1 ≤ j ≤ N+1 ⟹ j ≤ N. The Q⁻=∅ branch handles J=N+1 reflexively. The Q⁻≠∅ branch applies the IH restricted to {j: 1 ≤ j ≤ N} and dispatches the (g.(N+1), g.J′) comparison by T1's trichotomy: case g.J′ ≤ g.(N+1) sets J=J′ (IH covers Q⁻, direct comparison covers N+1); case g.(N+1) < g.J′ sets J=N+1 (mixed chain g.(N+1) < g.J′ ≤ g.j closed by < -transitivity and equality substitution). All cases covered. ✓

- *Instantiation*: g := f (from S8-fin, into dom ⊆ T), Q := Q₀ = {j: f.j ∈ V_1(d)}. V_1(d) ≠ ∅ forces Q₀ ≠ ∅ via f's surjectivity onto dom ⊇ V_1(d). The result f.J ≤ f.j for all j ∈ Q₀ extends to f.J ≤ v for all v ∈ V_1(d) because every v ∈ V_1(d) is reached by some j ∈ Q₀. ✓

**D-MIN — uniqueness.** Two least elements μ, μ′ give μ ≤ μ′ and μ′ ≤ μ. The argument uses T1's exactly-one postcondition (b), which includes ¬(a<b ∧ b<a); at a=b this yields ¬(a<a) (irreflexivity), covering the μ′=μ sub-case of μ′≤μ when μ<μ′ is assumed. Cases are exhausted; μ=μ′. ✓

**D-MIN — Depends list completeness.** Every symbol consumed by the formal contract and the body proof is cited: V-sub (V_1(d)), S8-depth (common depth m), T0 (comprehension witness for [1,...,1]), NAT-closure (literal 1 in the tuple and left-identity in the step), T1 (tumbler order), NAT-induction (existence proof), NAT-order (segment-identity reasoning on ℕ), NAT-addcompat (N<N+1, right-order compatibility for 1≤N+1), NAT-zero (0≤N seed), NAT-discrete (⊆ direction), S8-fin (enumerating bijection). NAT-wellorder and NAT-cancel are correctly absent.

**D-MIN — non-derivability witness.** The counterexample {[1,5],[1,6],[1,7]} is correctly informal and correctly identifies D-CTG's depth guard as the reason contiguity is satisfied, without needing D-CTG's full formal definition here.

**Cross-claim consistency.** V-sub's V_1(d) ⊆ dom(Σ.M(d)) is grounded at V-sub's own definition and used in D-MIN via S8-fin's enumeration. S8-depth's per-state common depth m is well-defined whenever V_1(d) ≠ ∅ (pick any u ∈ V_1(d), m = #u, uniformity from S8-depth). T0's comprehension at p=m ≥ 1 (T0's nonemptiness guarantees m ≥ 1) instantiated with constant map r≡1 yields the all-ones tuple. No cross-claim inconsistency found.

VERDICT: CONVERGED