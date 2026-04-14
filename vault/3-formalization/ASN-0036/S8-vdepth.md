**S8-vdepth (MinimalVPositionDepth).** Every V-position in the arrangement has tumbler depth at least 2:

`(A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`

This is not an independent axiom but a consequence of the structural chain S8a → S3 → S7c. For any V-position v ∈ dom(Σ.M(d)): S8a establishes that v is the element field of the I-address a = M(d)(v); S3 guarantees a ∈ dom(Σ.C); and S7c requires #fields(a).element ≥ 2. Since v = fields(a).element, we have #v ≥ 2. ∎

The consequence is load-bearing throughout. At `#v = 1`, a V-position `v = [s]` would consist of the subspace identifier alone, and OrdinalShift's last-component increment would modify `s` itself — the shift would change the subspace rather than advancing within it. S8-vdepth eliminates this case: every V-position has `#v ≥ 2`, so the subspace identifier `v₁` lies strictly before the action point `#v`, and ordinal shifts advance within the subspace without altering its identity. Gregory's evidence confirms `#v = 2` as the standard pattern: V-addresses consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal.

*Formal Contract:*
- *Theorem:* `(A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`
- *Preconditions:* S8a (V-positions are element-field tumblers); S3 (referential integrity: M(d)(v) ∈ dom(Σ.C)); S7c (element-field depth ≥ 2 for all content addresses).
- *Proof:* For v ∈ dom(Σ.M(d)), let a = M(d)(v). By S3, a ∈ dom(Σ.C). By S8a, v = fields(a).element. By S7c, #fields(a).element ≥ 2. Therefore #v ≥ 2.
