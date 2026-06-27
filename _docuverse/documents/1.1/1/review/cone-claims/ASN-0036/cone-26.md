Dependency graph, subspace guards, and case structure read clean across all claims. The only item that warrants a finding is in D-CTG-depth.

### D-CTG-depth reduction step: NAT-wellorder absent from depends
**Class**: REVISE
**Foundation**: NAT-wellorder (NatWellOrdering)
**ASN**: D-CTG-depth (SharedPrefixReduction), reduction-step paragraph: *"Suppose otherwise. Let j be the least component in the range 1 ≤ j ≤ m − 1 at which v differs from u"*; and, at the earlier contradiction setup: *"whose first point of disagreement is at component j with 2 ≤ j ≤ m − 1"*
**Issue**: Both uses name a minimum element of a non-empty subset of ℕ. Extracting the least j from {i ∈ {1,...,m−1} : vᵢ ≠ uᵢ} (reduction step) or from {i ∈ {2,...,m−1} : uᵢ ≠ xᵢ} (contradiction setup) is a direct application of the least-element principle, which is exactly what NAT-wellorder supplies. TumblerAdd cites NAT-wellorder for the identical pattern ("least element of {j : 1 ≤ j < k ∧ aⱼ > 0} in the divergence sub-case"). D-CTG-depth performs the same construction twice but NAT-wellorder does not appear in its depends list.
**What needs resolving**: Add NAT-wellorder (NatWellOrdering) to D-CTG-depth's depends, citing it at both the "first point of disagreement" invocation in the contradiction setup and the "least component" construction in the reduction step.

---

Everything else is sound:

- **D-CTG**: Invariant posit; guards are well-typed against T, subspace, T4, T1, T0; no proof needed.
- **S8-depth**: Design posit; the acknowledged overreach (link/annotation subspaces ungrounded) is explicitly bounded so it opens no gap in the claims that consume it; S8-depth is instantiated only at subspace 1 in D-CTG-depth's preconditions.
- **S8a**: The two-step derivation `zeros(t)=0 ⟺ S=∅ ⟺ (∀i: tᵢ>0)` via NAT-card → NAT-zero is correct; depends complete.
- **V-sub**: Clean restriction; disjointness of subspace projections follows immediately from `subspace(v) = v₁` being single-valued.
- **OrdShiftHom**: Both parts correct. Part (a) uses copy-region position 1 (valid since m ≥ 2). Part (b) closes the action-point component via OrdinalShift's postcondition `rₘ = vₘ + n ≥ 1` rather than re-deriving from ℕ arithmetic.
- **D-CTG-depth first postcondition**: The finiteness contradiction is fully walked. Witness w is grounded in T via T0 comprehension; S8a is discharged for w before D-CTG is applied; T0(a) iteratively supplies strictly increasing n-values; T3 separates distinct witnesses; S8-fin closes the contradiction.
- **D-CTG-depth second postcondition**: Forward direction reduces to a contradiction with T1 trichotomy (x < v vs. v < x) once u and x are known to share components 1..m−1. Backward direction assembles u < v < x from T1(i) at k = m, using the first postcondition to supply xᵢ = uᵢ for i ≤ m−1. The note that the prefix conjunct is load-bearing is verified by example.
- **Cross-claim coherence**: No circular dependencies; D-CTG-depth depends on D-CTG but not vice-versa; OrdShiftHom depends on S8a but not vice-versa.

VERDICT: REVISE