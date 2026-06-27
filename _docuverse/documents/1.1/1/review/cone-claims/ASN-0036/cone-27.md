The dependency graph is well-formed: D-CTG-depth depends on established foundations (T0, T0(a), T1, T3, NAT-wellorder) and ASN-0036 posits (D-CTG, S8a, S8-depth, S8-fin), with V-sub and subspace supplying the text-subspace projection machinery. OrdShiftHom depends cleanly on ASN-0034 foundations (OrdinalShift, OrdinalDisplacement, TumblerAdd, TA0).

**OrdShiftHom** is sound. Part (a) routes the subspace identity through the copy-region bound m ≥ 2, giving r₁ = v₁ directly without invoking S8-depth. Part (b) combines the S8a hypothesis (vᵢ ≥ 1 for i < m) with OrdinalShift's exported component lower bound (rₘ = vₘ + n ≥ 1) to close all component-positivity obligations. The instance [1,3,5], n=2 checks out.

**D-CTG-depth first postcondition**: The contradiction construction is complete. NAT-wellorder is correctly applied to the interior index subset of ℕ. T0 comprehension grounds the witness w as a genuine tumbler (all components ℕ-valued, length m ≥ 1). All D-CTG guard conditions are verified for w (subspace = 1 via w₁ = u₁ = 1 since j ≥ 2, depth m = #u, zeros = 0 from all-positive components, betweenness u < w < x via T1(i) at k = j+1 and k = j respectively). T0(a) is correctly instantiated at t = u ∈ T, i = j+1, successive bounds, extracting the strictly-increasing n-sequence. T3 witnesses distinctness of the resulting w-values. S8-fin delivers the finiteness contradiction.

**D-CTG-depth second postcondition**: The reduction is sound in both directions. Forward: the first-differing-component argument via T1(i) and trichotomy correctly forces any guard-admitted v between u and x to share the prefix 1..m-1; the note that the prefix conjunct is load-bearing is correct (e.g., m = 3, u = [1,5,3], x = [1,5,7], v = [1,6,5] satisfies u₃ < v₃ < x₃ but v > x). Reverse: T1(i) at k = m lifts uₘ < vₘ and vₘ < xₘ to the full ordering directly.

The acknowledged overreach in S8-depth (quantifier covers all subspaces, evidence grounds only text) is correctly scoped out: no claim instantiates S8-depth at non-text positions.

One presentation gap:

### Reduction step leaves j ≥ 2 implicit
**Class**: OBSERVE
**Foundation**: D-CTG-depth (SharedPrefixReduction), second postcondition proof (reduction step); subspace (VPositionSubspaceIdentifier)
**ASN**: D-CTG-depth reduction step: "Let j be that least component, 1 ≤ j ≤ m − 1 … the hypothesis u < v therefore yields uⱼ < vⱼ."
**Issue**: NAT-wellorder extracts j as the minimum of {i : 1 ≤ i ≤ m − 1 ∧ vᵢ ≠ uᵢ}; the proof states "1 ≤ j ≤ m − 1" and immediately applies T1(i) at j as the first overall differing component between u and v. This application requires j ≥ 2: the outer-quantifier guard subspace(v) = 1 gives v₁ = 1, and u ∈ V_1(d) gives u₁ = 1, so v₁ = u₁ and position 1 is not in {i : vᵢ ≠ uᵢ}, making j ≥ 2. The proof does not state this; a reader following the "1 ≤ j" bound must trace back through the guards independently to verify that T1(i) at j is the first overall differing component.
**What needs resolving**: Add a one-line note before applying T1: since subspace(v) = 1 (outer-quantifier guard) and u ∈ V_1(d) both yield component 1 equal to 1, position 1 is not in {i : 1 ≤ i ≤ m − 1 ∧ vᵢ ≠ uᵢ}, so j ≥ 2. The agreement on 1..j − 1 established by NAT-wellorder's minimality then covers the full leading-component range required for T1(i) to identify j as the first overall differing component.

VERDICT: OBSERVE