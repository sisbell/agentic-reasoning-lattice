**S8-depth(a) (ConsecutiveVPositions).** Within a subspace `s` of document `d`, V-positions are *consecutive* when they differ only at the ordinal (last) component: position `s.x` is followed by `s.(x+1)`. This notion is well-defined because S8-depth guarantees that all V-positions in subspace `s` share a common depth `m` — the "last component" is unambiguous, and consecutive positions satisfy `(v₁)ᵢ = (v₂)ᵢ` for all `1 ≤ i < m` with `(v₂)_m = (v₁)_m + 1`.

*Formal Contract:*
- *Precondition:* `v₁, v₂ ∈ dom(Σ.M(d))`, `subspace(v₁) = subspace(v₂) = s`
- *Definition:* `v₁` and `v₂` are consecutive in subspace `s` iff `(v₁)ᵢ = (v₂)ᵢ` for all `1 ≤ i < m` (where `m = #v₁ = #v₂` by S8-depth) and `(v₂)_m = (v₁)_m + 1`
- *Dependencies:* S8-depth
