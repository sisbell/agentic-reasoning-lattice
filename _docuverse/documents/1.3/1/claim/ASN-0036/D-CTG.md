**D-CTG (VContiguity).** For each document d, the text-subspace projection V_1(d) — the active text V-positions `{v ∈ dom(Σ.M(d)) : subspace(v) = 1}` of d, as defined in V-sub (SubspaceProjection) — is either empty or occupies every intermediate position between its extremes:

`(A d, u, q : u ∈ V_1(d) ∧ q ∈ V_1(d) ∧ u < q : (A v ∈ T : subspace(v) = 1 ∧ #v = #u ∧ zeros(v) = 0 ∧ u < v < q : v ∈ V_1(d)))`

The candidate position v ranges over the tumbler carrier set T (T0, CarrierSetDefinition, ASN-0034); this domain is what makes the inner guards well-typed, since the component projection `subspace(v) = v₁`, the length `#v`, and the strict order `<` in `u < v < q` (the last from T1, LexicographicOrder) are all defined only on T. The guards then restrict v to the same-depth, zero-free text-subspace positions strictly between u and q.

In words: within the text subspace, V-positions form a contiguous ordinal range with no gaps. If positions [1, 3] and [1, 7] are occupied, then every position [1, k] with 3 < k < 7 must also be occupied.

For the text subspace at depth m = 2, this is a finite condition: the intermediates between [1, a] and [1, b] are the finitely many [1, i] with a < i < b. This betweenness statement is all that D-CTG asserts; the stronger reading — that V_1(d) occupies a *single unbroken block* of ordinals — is not a consequence of contiguity alone but of contiguity combined with the arrangement's finiteness, and is derived in D-SEQ, the claim that brings both ingredients together.

- *Depends:*
  - V-sub (SubspaceProjection) — supplies the definition of the text-subspace projection `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}` over which the contiguity statement quantifies; the extreme guards `u ∈ V_1(d)`, `q ∈ V_1(d)` and the consequent `v ∈ V_1(d)` are membership tests against this set, each unfolding to `· ∈ dom(Σ.M(d)) ∧ subspace(·) = 1`
  - subspace (VPositionSubspaceIdentifier) — supplies the projection `subspace(v) = v₁`, the function whose value the inner-quantifier guard `subspace(v) = 1` constrains, restricting each intermediate position v to the text subspace (subspace identifier 1)
  - T4 (HierarchicalParsing, ASN-0034) — supplies the zero-count `zeros`, grounding the inner-quantifier guard `zeros(v) = 0` that restricts the intermediate position v to a zero-free V-position
  - T1 (LexicographicOrder, ASN-0034) — supplies the strict order `<` on tumblers used in the extremes guard `u < q` and the betweenness guard `u < v < q` that delimit the intermediate positions
  - T0 (CarrierSetDefinition, ASN-0034) — supplies the tumbler carrier set `T`, the domain of the inner quantifier's candidate v (without which the guard terms `subspace(v)`, `#v`, and `u < v < q` are ill-typed); and the tumbler length `#`, giving meaning to the same-depth selector `#v = #u`