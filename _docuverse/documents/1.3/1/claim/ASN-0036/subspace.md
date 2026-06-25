**subspace (VPositionSubspaceIdentifier).** For any tumbler `v` of depth `#v ≥ 1`, define:

`subspace(v) = v₁`

extracting the subspace identifier as the first component of a V-position.

*Formal Contract:*
- *Signature:* `subspace : T → ℕ` — projects the first component of a tumbler.
- *Preconditions:* `v ∈ T`, `#v ≥ 1` (so that `v₁` is well-defined as the first component of a non-empty tumbler).
- *Definition:* `subspace(v) = v₁`.
