**V-sub (SubspaceProjection).** The arrangement-contiguity invariants speak not of the whole arrangement domain `dom(Σ.M(d))` but of one subspace at a time — Nelson's "addresses 1 through 100" is a statement about the *text* subspace, not about link or annotation positions that may share the same document. We therefore name the object those invariants range over. For a document `d` and a subspace identifier `S`, the *subspace projection* `V_S(d)` is the set of active V-positions of `d` whose subspace identifier is `S`:

`V_S(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = S}`

The set is carved out of the arrangement domain `dom(Σ.M(d))` (Σ.M(d), Arrangement) by the membership guard `subspace(v) = S`, where `subspace(v) = v₁` (subspace, VPositionSubspaceIdentifier) reads the subspace identifier off the first component of the V-position. Hence `V_S(d) ⊆ dom(Σ.M(d))` for every `S`; and since `subspace` assigns each active position the single value `v₁`, distinct subspaces yield disjoint projections — every active V-position lands in exactly the projection of its own subspace.

The case the arrangement-contiguity invariants single out is the *text subspace*, `S = 1`. We write its projection as

`V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}`

— the active text V-positions of `d`. This is the symbol D-CTG, D-CTG-depth, D-MIN, and D-SEQ constrain; the present claim is what gives it meaning, fixing `v ∈ V_1(d)` as the conjunction `v ∈ dom(Σ.M(d)) ∧ subspace(v) = 1`. The definition introduces no constraint of its own beyond this restriction of the arrangement domain by a subspace identifier.

*Formal Contract:*

- *Definition:* For a document `d` and subspace identifier `S`, `V_S(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = S}` — the active V-positions of `d` whose first component is `S`. Membership `v ∈ V_S(d)` unfolds to `v ∈ dom(Σ.M(d)) ∧ subspace(v) = S`, so `V_S(d) ⊆ dom(Σ.M(d))` for every `S`. The text-subspace specialization is `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}`, equivalently `v ∈ V_1(d) ⟺ v ∈ dom(Σ.M(d)) ∧ subspace(v) = 1`.

- *Depends:*
  - Σ.M(d) (Arrangement) — supplies the arrangement `Σ.M(d)` and its domain `dom(Σ.M(d))`, the set of active V-positions the projection restricts; `V_S(d)` is by definition a subset of `dom(Σ.M(d))`
  - subspace (VPositionSubspaceIdentifier) — supplies the selector `subspace(v) = v₁`, the function whose value the membership guard `subspace(v) = S` constrains, sorting each active V-position into the projection of its own subspace
- *Forward References:*
  - D-CTG (VContiguity) — consumes V_1(d) as the set over which its contiguity quantifier ranges; this claim is what gives that set meaning
  - D-CTG-depth (SharedPrefixReduction) — consumes V_1(d) as the text-subspace projection whose elements it proves share a common prefix; defined here
  - D-MIN (VMinimumPosition) — constrains min(V_1(d)) to the all-ones tuple; V_1(d) is the set defined here
  - D-SEQ (SequentialPositions) — derives the sequential form of V_1(d) by composing D-CTG, D-CTG-depth, and D-MIN over the set defined here
