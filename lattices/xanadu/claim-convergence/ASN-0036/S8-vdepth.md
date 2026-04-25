**S8-vdepth (MinimalVPositionDepth).** Every V-position in the arrangement has tumbler depth at least 2:

`(A d ∈ D, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`

This is a design requirement on the V-position space, parallel to S8a's well-formedness constraint and S8-depth's fixed-depth constraint. The derivation previously claimed — that S8a identifies `v` with `fields(a).element` for `a = M(d)(v)`, whence S7c's bound `#fields(a).element ≥ 2` transfers to `#v` — rests on an unstated structural identification between V-positions and I-address element fields. S8a constrains V-position component values (`zeros(v) = 0`, `v₁ ≥ 1`); S3 constrains `M(d)`'s range (`M(d)(v) ∈ dom(Σ.C)`); S7c constrains I-address element-field depth (`#fields(a).element ≥ 2`). None establishes that a V-position equals the element field of its mapped I-address. The step from "the I-address mapped to by `v` has element-field depth ≥ 2" to "`v` itself has ≥ 2 components" requires a structural bridge — a model constraint relating V-position depth to I-address element-field depth — that the current property set does not provide. S8-vdepth is therefore stated as an independent axiom.

The constraint is load-bearing throughout. At `#v = 1`, a V-position `v = [s]` would consist of the subspace identifier alone, and OrdinalShift's last-component increment would modify `s` itself — the shift would change the subspace rather than advancing within it. S8-vdepth eliminates this case: every V-position has `#v ≥ 2`, so the subspace identifier `v₁` lies strictly before the action point `#v`, and ordinal shifts advance within the subspace without altering its identity. Gregory's evidence confirms `#v = 2` as the standard pattern: V-addresses consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal.

*Formal Contract:*
- *Axiom:* `(A d ∈ D, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`
