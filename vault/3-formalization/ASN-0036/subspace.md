**subspace(v) (SubspaceIdentifier).** The subspace identifier of a V-position v:

`subspace(v) = v₁`

The first component of an element-field tumbler identifies which subspace the position belongs to (1 for text, 2 for links). By S8a, v₁ ≥ 1 for all V-positions.

*Formal Contract:*
- *Definition:* `subspace(v) = v₁` for v ∈ dom(Σ.M(d)).
- *Preconditions:* S8a — v₁ ≥ 1.
- *Postconditions:* subspace(v) ≥ 1.
