**subspace(v) (SubspaceIdentifier).** For a tumbler v with #v ≥ 1, the subspace identifier is the first-component extraction:

`subspace(v) = v₁`

Since v₁ is defined for any tumbler with at least one component, subspace applies throughout T wherever #v ≥ 1 — including contexts where V-position membership has not yet been established (D-CTG's inner quantifier, OrdAddHom's result tumbler, D-CTG-depth's constructed intermediates). For V-positions (elements of dom(Σ.M(d))), the subspace identifier distinguishes which subspace the position belongs to (1 for text, 2 for links). (Note: for V-positions, S8a separately guarantees v₁ ≥ 1.)

*Formal Contract:*
- *Definition:* `subspace(v) = v₁` for `v ∈ T` with `#v ≥ 1`.
- *Preconditions:* `v ∈ T`, `#v ≥ 1`.
- *Postconditions:* `subspace(v) ∈ ℕ`.
