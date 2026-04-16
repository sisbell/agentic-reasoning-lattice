**ActionPoint (ActionPoint).** For w ∈ T with Pos(w), the *action point* of w is actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}). Since Pos(w), PositiveTumbler guarantees at least one component of w is nonzero, so the set {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is nonempty and the minimum exists. From this definition, 1 ≤ actionPoint(w) ≤ #w, wᵢ = 0 for all i < actionPoint(w), and w_{actionPoint(w)} ≥ 1. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, Pos(w)
- *Definition:* actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; wᵢ = 0 for all i < actionPoint(w); w_{actionPoint(w)} ≥ 1
