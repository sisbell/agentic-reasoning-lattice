**D-CTG-S8a (ContiguityWellFormedness).** D-CTG and S8a are jointly satisfiable: every tumbler that D-CTG forces into V_S(d) automatically satisfies S8a's all-positive-components constraint.

`(A d, S, u, q, v : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q ∧ subspace(v) = S ∧ #v = #u ∧ u < v < q : zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`

D-CTG's universal quantifier ranges over all tumblers v with the specified subspace, depth, and ordering — including, in principle, tumblers with zero components. If such a tumbler satisfied the antecedent, D-CTG would force it into dom(M(d)), conflicting with S8a's requirement that every element of dom(M(d)) has all-positive components. We show no such tumbler can lie between any two elements of V_S(d).

*Proof.* Let V_S(d) be non-empty with common depth m (S8-depth), m ≥ 2 (S8-vdepth), and let u, q ∈ V_S(d) with u < q. By D-SEQ (SequentialPositions), V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n} for some n ≥ 1, where each tuple has length m. In particular, u = [S, 1, …, 1, k₁] and q = [S, 1, …, 1, k₂] with 1 ≤ k₁ < k₂ ≤ n.

Let v be any tumbler with subspace(v) = S, #v = m, and u < v < q. We show every component of v is strictly positive.

The first component v₁ = S, and S ≥ 1: by S8a applied to u (which belongs to dom(M(d))), u₁ = S ≥ 1.

For the intermediate components, suppose v first disagrees with u at some component j with 2 ≤ j ≤ m − 1. Then vᵢ = uᵢ for all i < j, and since u < v, T1(i) (LexicographicOrder, ASN-0034) gives vⱼ > uⱼ = 1, so vⱼ ≥ 2. But v and q agree on components 1 through j − 1 (since u and q share those components by D-SEQ's characterization, and v agrees with u there), and at component j, vⱼ ≥ 2 > 1 = qⱼ. By T1(i), v > q — contradicting v < q. Therefore v agrees with u on all components 1 through m − 1, each of which equals 1. Every intermediate component of v is positive. (At m = 2, the range 2 ≤ j ≤ m − 1 is empty, so this case holds vacuously.)

For the last component, since v agrees with u on components 1 through m − 1, the first point of disagreement between u and v is at component m. The condition u < v and T1(i) give vₘ > uₘ = k₁ ≥ 1, so vₘ ≥ 2. The last component is positive.

Every component of v is strictly positive: v₁ = S ≥ 1, components 2 through m − 1 are each 1, and vₘ ≥ 2. Therefore zeros(v) = 0 (no component equals zero), v₁ ≥ 1, and v > 0 (at least one nonzero component, satisfied a fortiori). Any tumbler forced into V_S(d) by D-CTG satisfies S8a. ∎

*Formal Contract:*
- *Preconditions:* D-SEQ (SequentialPositions) — V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}; S8-depth (FixedDepthVPositions) — common depth m; S8-vdepth (MinimalVPositionDepth) — m ≥ 2; S8a (VPositionWellFormedness) — existing V-positions have all-positive components.
- *Postconditions:* `(A d, S, u, q, v : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q ∧ subspace(v) = S ∧ #v = #u ∧ u < v < q : zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)` — every tumbler that D-CTG's universal quantifier could force into V_S(d) satisfies S8a's well-formedness constraint. D-CTG and S8a are jointly satisfiable in all non-trivial states.
