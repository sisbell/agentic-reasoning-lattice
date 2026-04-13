**S8-vdepth (MinimalVPositionDepth).** Every V-position in the arrangement has tumbler depth at least 2:

`(A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`

This is a design requirement, parallel to S7c for I-addresses. At `#v = 1`, a V-position `v = [s]` consists of the subspace identifier alone. The ordinal displacement `δ(k, 1)` has its action point at position 1, so `shift(v, k)` modifies `s` itself — the shift changes the subspace rather than advancing within it. At `#v ≥ 2`, the subspace identifier `v₁` lies strictly before the action point `#v`, so TumblerAdd’s prefix rule copies it unchanged; ordinal shifts advance within the subspace without altering its identity. Gregory’s evidence confirms `#v = 2` as the standard pattern: V-addresses consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal.

*Formal Contract:*
- *Axiom:* `(A d, v : v ∈ dom(Σ.M(d)) : #v ≥ 2)`
