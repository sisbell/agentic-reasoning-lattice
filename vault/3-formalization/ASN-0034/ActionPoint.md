**ActionPoint (ActionPoint).** For w ∈ T with Pos(w), the *action point* of w is actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}). Since Pos(w), PositiveTumbler guarantees at least one component of w is nonzero, so the set {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is nonempty and the minimum exists. From this definition, 1 ≤ actionPoint(w) ≤ #w, wᵢ = 0 for all i < actionPoint(w), and w_{actionPoint(w)} ≥ 1. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w)
- *Definition:* actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})
- *Depends:* T0 (CarrierSetDefinition) — the precondition `w ∈ T`, the length `#w`, and the component projection `wᵢ` used in the definition and postconditions all come from T0's characterisation of T as finite sequences over ℕ with length ≥ 1. PositiveTumbler (PositiveTumbler) — supplies the predicate `Pos(w)` in the precondition and guarantees the existence of an index `i` with `wᵢ ≠ 0`, making the set `{i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}` nonempty so that the `min` in the definition is well-defined.
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; wᵢ = 0 for all i < actionPoint(w); w_{actionPoint(w)} ≥ 1
