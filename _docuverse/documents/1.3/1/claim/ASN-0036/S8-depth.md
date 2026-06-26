**S8-depth (FixedDepthVPositions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)`

Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. Any correct implementation must satisfy this constraint.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: a position `v` is followed by `shift(v, 1)` (equivalently `v ⊕ δ(1, #v)` per OrdinalShift, ASN-0034), the next ordinal at the same depth.

### Shift preservation for V-positions

For the successor `shift(v, 1)` to be itself a V-position of the same subspace — so that "consecutive V-positions" is a well-formed notion — ordinal shift must leave a V-position's subspace identifier and its S8a well-formedness intact. It does, and we do not re-derive it here: OrdShiftHom (OrdinalShiftPreservation) establishes both halves — part (a), `subspace(shift(v, n)) = subspace(v)`, and part (b), `shift(v, n)` satisfies S8a whenever `v` does. We invoke OrdShiftHom wherever a shifted V-position must be shown to remain in its subspace and well-formed.

- *Depends:*
  - subspace (VPositionSubspaceIdentifier) — supplies the projection `subspace(·) = (·)₁` whose equality `subspace(u) = subspace(w)` is the range restriction in S8-depth's formal statement, selecting the pairs of V-positions that share a subspace identifier
  - OrdinalShift (ASN-0034) — supplies the `shift(v, n)` operator and `δ` displacement operator used to define consecutive V-positions: `v` is followed by `shift(v, 1) = v ⊕ δ(1, #v)`
  - OrdShiftHom (OrdinalShiftPreservation) — supplies the shift-preservation result this section invokes rather than re-deriving: `shift(v, n)` preserves a V-position's subspace identifier (part a) and its S8a well-formedness (part b), so the successor `shift(v, 1)` of a V-position is itself a V-position of the same subspace
  - S8a (ArrangementDomainRestriction) — supplies the well-formedness predicate (`zeros(t) = 0 ∧ #t ≥ 2`) named as the property OrdShiftHom shows `shift(v, n)` preserves