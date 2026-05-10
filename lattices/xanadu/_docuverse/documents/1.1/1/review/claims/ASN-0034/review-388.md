# Regional Review — ASN-0034/ActionPoint (cycle 1)

*2026-04-22 23:17*

### ActionPoint uniqueness proof appeals to unstated "exclusivity"
**Class**: REVISE
**Foundation**: NAT-order (NatStrictTotalOrder) — totality clause is "at least one" (`m < n ∨ m = n ∨ n < m`), not exclusive trichotomy.
**ASN**: ActionPoint *Derivation*, uniqueness step: "NAT-order's trichotomy excludes both m₁ < m₂ (which would force the disjunct m₂ < m₁ ∨ m₂ = m₁ in m₂ ≤ m₁ to land on m₂ < m₁, violating trichotomy's exclusivity against m₁ < m₂) and m₂ < m₁ (symmetrically), leaving m₁ = m₂."
**Issue**: NAT-order's *Axiom* slot states totality as a non-exclusive disjunction. "Trichotomy's exclusivity" is not a contract clause; it must be derived from irreflexivity + transitivity. Additionally, when m₁ ≤ m₂ unfolds to `m₁ < m₂ ∨ m₁ = m₂` and m₂ ≤ m₁ unfolds to `m₂ < m₁ ∨ m₂ = m₁`, the proof handles only the cross case (m₁ < m₂ paired with m₂ < m₁) and does not address the case where, say, m₁ < m₂ pairs with m₂ = m₁ — which collapses to m₁ < m₁ and contradicts irreflexivity directly. The current text claims the disjunct "lands on" m₂ < m₁ without justifying why the equality disjunct is excluded.
**What needs resolving**: The uniqueness argument should either (a) walk all four disjunct pairings using only stated axioms (irreflexivity, transitivity, the definition of ≤), or (b) cite an antisymmetry/exclusivity lemma after deriving it explicitly from those axioms. The appeal to an unstated "exclusivity" property of trichotomy must be removed or grounded.

### Meta-prose about axiomatization register
**Class**: OBSERVE
**Foundation**: n/a (internal style)
**ASN**: NAT-order: "NAT-closure follows the same register for the arithmetic primitive…"; NAT-closure: "The operation is posited directly on ℕ rather than derived from an earlier axiom — the same register NAT-order uses…"; TA-Pos: "the explicit `i ∈ ℕ` keeps parity with the `(A n ∈ ℕ :: …)` form used by the sibling NAT axioms."
**Issue**: These passages explain *why the axiom is presented in a particular form* (parity, register, sibling style) rather than what the axiom asserts. They do not advance reasoning and are the kind of defensive justification that compounds across cycles.

### `tᵢ ≠ 0` vs `¬(tᵢ = 0)` lexical drift
**Class**: OBSERVE
**Foundation**: n/a
**ASN**: TA-Pos defines Pos via `¬(tᵢ = 0)`; ActionPoint's set S uses `wᵢ ≠ 0`.
**Issue**: Same predicate written two ways within one ASN. Semantically identical, but a precise reader has to confirm that.

VERDICT: REVISE
