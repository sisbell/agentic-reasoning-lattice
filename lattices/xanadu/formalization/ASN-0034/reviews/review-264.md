# Cone Review — ASN-0034/TS2 (cycle 5)

*2026-04-18 08:43*

### OrdinalDisplacement does not export `#δ(n, m) = m` as a named postcondition; OrdinalShift's proof consumes this fact without citation
**Foundation**: OrdinalDisplacement — Postconditions list `δ(n, m) ∈ T (by T0), Pos(δ(n, m)) (by TA-Pos), actionPoint(δ(n, m)) = m (by ActionPoint)`. Length of δ is stated only within the Definition clause.
**ASN**: OrdinalShift proof, result-length derivation: "By TumblerAdd: shift(v, n)ᵢ = vᵢ for i < m, shift(v, n)ₘ = vₘ + n, and #shift(v, n) = #δ(n, m) = m = #v."
**Issue**: The equality `#δ(n, m) = m` is the load-bearing step that bridges TumblerAdd's result-length identity `#(a ⊕ w) = #w` (which gives `#shift(v, n) = #δ(n, m)`) to OrdinalShift's postcondition `#shift(v, n) = #v`. The fact is apparent from the Definition phrasing ("of length m") but is not promoted to a named postcondition of OrdinalDisplacement, and OrdinalShift's proof consumes it silently — without citing any source. The three other facts about δ (membership, positivity, action point) are each explicitly promoted to named postconditions and cited verbatim downstream; the length fact is not, breaking the per-step routing discipline OrdinalShift's own Depends enforces at every other δ-fact consumption site. TS2's proof inherits the gap when it uses "m" as both `#v₁ = #v₂` and implicitly `#δ(n, m)`.
**What needs resolving**: Either OrdinalDisplacement must export `#δ(n, m) = m` as a named postcondition (paralleling the other three), with OrdinalShift citing it at the `#δ(n, m) = m` step; or OrdinalShift must route the step through another named source (e.g., OrdinalDisplacement's Definition, cited by name).

### TS2 formal statement contains a free variable `m` with no binder
**Foundation**: Precision of quantifier scope — every variable in a formal statement must be bound by a quantifier or by an enclosing parameter.
**ASN**: TS2 statement: "`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`".
**Issue**: The universal quantifier binds `v₁, v₂, n`. The range conjunct `#v₁ = #v₂ = m` contains `m`, which is not bound by the quantifier, not introduced as a parameter at an outer scope, and not declared elsewhere in the TS2 Formal Contract (which restates `#v₁ = #v₂ = m` in Preconditions with the same free `m`). A reader cannot tell whether `m` is implicitly existentially quantified (equivalent to `#v₁ = #v₂`), universally quantified at an outer scope, or a named parameter. Sister properties in the ASN that state a shared length introduce it by either explicit quantification or by equality to a defined expression. The free `m` also propagates into the Preconditions list, where it appears unbound.
**What needs resolving**: TS2 must bind `m` explicitly — either by dropping `m` and writing `#v₁ = #v₂`, or by adding `m` to the quantifier (e.g., `(A v₁, v₂ ∈ T, n ∈ ℕ, m : …)`), with the Preconditions list updated to match. The binding convention should align with how other ASN properties introduce shared length parameters.

## Result

Cone converged after 6 cycles.

*Elapsed: 3327s*
