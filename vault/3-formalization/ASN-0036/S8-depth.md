**S8-depth (Fixed-depth V-positions).** Within a given subspace `s` of document `d`, all V-positions share the same tumbler depth:

`(A d, p, q : p ∈ dom(Σ.M(d)) ∧ q ∈ dom(Σ.M(d)) ∧ p₁ = q₁ : #p = #q)`

This is a design requirement, not a convention — parallel to S7a. Gregory's evidence supports it: V-addresses in the text subspace consistently use the form `s.x` — two tumbler digits, where `s` is the subspace identifier and `x` is the ordinal. The two-blade knife computation (which sets the second blade at `(N+1).1` for any insertion at `N.x`) works only if all positions within a subspace share the same depth. Any correct implementation must satisfy this constraint.

We establish the invariant by induction over the operation history.

*Base case.* By AX-1 (InitialEmptyState), `dom(Σ₀.M(d)) = ∅` for every document `d`. The universal quantification `(A d, p, q : p ∈ ∅ ∧ … : …)` holds vacuously — the empty domain contains no pair of positions that could violate uniform depth.

*Inductive step.* Suppose the constraint holds in state Σ: within each subspace, every occupied V-position has the same tumbler depth. Let Σ → Σ' be any state transition; by AX-5 (ClosedWorldTransition), some op ∈ Op produces Σ' from Σ. Each such operation either removes positions from a subspace — which cannot introduce a depth mismatch among the remaining positions — or introduces new positions into a subspace, which must share the depth of the positions already there (or, if the subspace was previously empty, must all share a common depth). Therefore `dom(Σ'.M(d))` satisfies fixed-depth.

This is a design requirement: every operation specification must individually discharge the obligation that it maps a state satisfying fixed-depth to another state satisfying fixed-depth. The base case and the closure argument above reduce that global invariant to a per-operation verification condition. ∎

*Formal Contract:*
- *Invariant:* `(A d, p, q : p ∈ dom(Σ.M(d)) ∧ q ∈ dom(Σ.M(d)) ∧ p₁ = q₁ : #p = #q)`
- *Preconditions:* `dom(M(d)) ⊆ T` (Σ.M(d)).
