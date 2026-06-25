**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)`

Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. Any correct implementation must satisfy this constraint.

*Formal Contract:*
- *Axiom (design requirement):* `(A d, u, w : u ∈ dom(Σ.M(d)) ∧ w ∈ dom(Σ.M(d)) ∧ subspace(u) = subspace(w) : #u = #w)`.
- *Postconditions:* Within a subspace `s` of document `d`, if `V_s(d) ≠ ∅` then there exists a common depth `m_s ≥ 2` (by S8a) such that every V-position with `v₁ = s` has length `m_s`. For empty `V_s(d)` no witness depth is asserted. Distinct subspaces may have distinct depths.
- *Depends:* S8a — for the lower bound `m_s ≥ 2`.

S8-depth allows us to define "consecutive V-positions" precisely. Within a subspace, consecutive positions differ only at the ordinal (last) component: a position `v` is followed by `shift(v, 1)` (equivalently `v ⊕ δ(1, #v)` per OrdinalShift, ASN-0034), the next ordinal at the same depth.

### Shift preservation for V-positions

Ordinal shift `shift(v, n)` (OrdinalShift, ASN-0034) preserves a V-position's subspace identifier and its S8a well-formedness, as the following lemma establishes.

- *Depends:*
  - S8a (Σ.M(d) domain restriction) — supplies the well-formedness constraint and lower bound m_s ≥ 2 used in the postconditions and the shift-preservation lemma
  - OrdinalShift (ASN-0034) — supplies the shift(v, n) operator and v ⊕ δ(1, #v) notation used to characterize consecutive V-positions and state the shift-preservation lemma