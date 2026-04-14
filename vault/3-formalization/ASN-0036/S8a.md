**S8a (VPositionWellFormedness).** Every V-position has all components strictly positive and contains no zero-valued separators:

`(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)`

This is a design requirement on the V-position space, parallel to S8-depth's fixed-depth constraint and S8-fin's finiteness constraint. V-positions are indices into the arrangement map Σ.M(d); the three conjuncts constrain their internal structure. The conjunct `zeros(v) = 0` requires that no component of a V-position is zero — V-positions carry no field-separator structure. The conjunct `v > 0` — every component is strictly positive — ensures that 1 is the smallest value any component can take. The conjunct `v₁ ≥ 1` is a specialisation of `v > 0` to the first component, stated explicitly because it is load-bearing: `v₁` serves as the subspace identifier, and S8's partition proof requires every V-position to belong to some subspace `S = v₁ ≥ 1` to invoke T5 and T10 for cross-subspace disjointness.

The positivity constraint is load-bearing for D-MIN: if V-position components could include 0, then `[S, 0, …, 0]` would precede `[S, 1, …, 1]` under T1, and the axiom that `min(V_S(d)) = [S, 1, …, 1]` would be inconsistent with the set of constructible positions. By requiring `v > 0` universally, we ensure that `[S, 1, …, 1]` is genuinely the least element of any non-empty subspace.

*Remark.* The shared vocabulary identifies a second subspace for links (v₁ = 2, per LM 4/30). Link-subspace V-positions satisfy the same `zeros(v) = 0` and `v > 0` constraints as text-subspace positions — both have strictly positive components. The subspace identifier (1 for text, 2 for links) is the first component; the `0` in tumbler notation (e.g., `N.0.U.0.D.0.2.1`) is a field separator, not a subspace identifier. Link-subspace arrangement semantics are deferred to a future ASN.

*Formal Contract:*
- *Axiom:* `(A v ∈ dom(Σ.M(d)) :: zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0)` — every V-position has strictly positive components and no separator structure. This is a design requirement: operations that construct or modify V-positions must produce tumblers with all components strictly positive.
- *Postconditions:* `zeros(v) = 0` (no separators), `v₁ ≥ 1` (valid subspace identifier), `v > 0` (all components strictly positive).
