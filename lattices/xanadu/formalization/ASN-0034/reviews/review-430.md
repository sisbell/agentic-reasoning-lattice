# Regional Review — ASN-0034/TA-RC (cycle 2)

*2026-04-23 03:55*

### Meta-prose typing paragraph in TA-Pos Definition
**Class**: OBSERVE
**Foundation**: N/A (internal)
**ASN**: TA-Pos Definition: *"The bound variable `i` is typed to ℕ because the projection `tᵢ` is defined by T0 only on the index domain `{1, …, #t} ⊆ ℕ` and the bounding relation `≤` is ℕ-typed; the explicit `i ∈ ℕ` keeps parity with the `(A n ∈ ℕ :: …)` form used by the sibling NAT axioms. `tᵢ` itself is a natural number by T0's carrier, the literal `0` against which it is compared is the `0 ∈ ℕ` posited by NAT-zero, the numeral `1` bounding the quantifier range is the `1 ∈ ℕ` posited by NAT-closure, and the relation `≤` bounding that range is the non-strict companion of `<` defined on ℕ by NAT-order…"*
**Issue**: This paragraph is defensive justification — a use-site inventory explaining why each symbol's type is ℕ rather than advancing any mathematical claim. The Depends list already discharges the typing obligations; restating them in prose ahead of the complementarity argument is the "essay content in a structural slot" the review guidance flags. Reader must skip past it to reach the reasoning (DeMorgan duality) that actually proves complementarity.

### Complementarity placed in its own contract slot rather than Postconditions
**Class**: OBSERVE
**Foundation**: N/A (internal)
**ASN**: TA-Pos Formal Contract structure — uses *Definition:* / *Complementarity:* / *Depends:*, with no *Postconditions:* slot, whereas TumblerAdd, TA0, ActionPoint, and T3 all expose their derived facts under *Postconditions:*.
**Issue**: The complementarity biconditional `(A t ∈ T :: Pos(t) ⟺ ¬Zero(t))` is a proven consequence (discharged via DeMorgan in the prose), not part of the predicates' definitions. Putting it in a bespoke *Complementarity:* slot makes it harder for downstream citers to locate — dependents typically look for derived facts in *Postconditions:*. Structural-slot inconsistency across sibling claims in the same ASN.

### Notation for "nonzero component" not uniform across sibling claims
**Class**: OBSERVE
**Foundation**: N/A (internal)
**ASN**: TA-Pos Definition writes `¬(tᵢ = 0)`; ActionPoint writes `wᵢ ≠ 0` in the set-builder `S = {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}`.
**Issue**: Two notations for the same predicate within one ASN, in claims that sit directly beside each other and feed each other (TA-Pos's existential witness is exactly an element of ActionPoint's S). The `≠` symbol is not formally introduced in either Depends list. A single choice — keeping parity with the explicit `¬(· = 0)` spelling used in TA-Pos, or introducing `≠` as shorthand — would avoid the implicit equivalence the reader must reconcile.

VERDICT: OBSERVE

## Result

Regional review converged after 2 cycles.

*Elapsed: 502s*
