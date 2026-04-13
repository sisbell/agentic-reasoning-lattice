**V_S(d) (SubspaceVPositionSet).** The set of V-positions in subspace S of document d:

`V_S(d) = {v ∈ dom(Σ.M(d)) : v₁ = S}`

V_S(d) partitions dom(Σ.M(d)) by subspace identifier. Every element of V_S(d) satisfies S8a (V-position well-formedness): zeros(v) = 0, v₁ ≥ 1, v > 0. Within V_S(d), all positions share a common depth by S8-depth.

*Formal Contract:*
- *Definition:* `V_S(d) = {v ∈ dom(Σ.M(d)) : v₁ = S}` for subspace identifier S ≥ 1 and document d.
- *Preconditions:* S8a — every v ∈ dom(Σ.M(d)) satisfies zeros(v) = 0 ∧ v₁ ≥ 1 ∧ v > 0.
