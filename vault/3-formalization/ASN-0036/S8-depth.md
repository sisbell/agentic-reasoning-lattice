**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, p, q : p ∈ dom(Σ.M(d)) ∧ q ∈ dom(Σ.M(d)) ∧ p₁ = q₁ : #p = #q)`

This is a design requirement, not a convention — parallel to S7a. Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth. Any correct implementation must satisfy this constraint.

*Formal Contract:*
- *Axiom:* `(A d, p, q : p ∈ dom(Σ.M(d)) ∧ q ∈ dom(Σ.M(d)) ∧ p₁ = q₁ : #p = #q)`
- *Preconditions:* `dom(M(d)) ⊆ T` (Σ.M(d)).
