**ActionPoint (ActionPoint).** For w ∈ T with w > 0, the *action point* of w is actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0}). Since w > 0, PositiveTumbler guarantees at least one component of w is nonzero, so the set {i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is nonempty and the minimum exists. From this definition, 1 ≤ actionPoint(w) ≤ #w, wᵢ = 0 for all i < actionPoint(w), and w_{actionPoint(w)} ≥ 1. ∎

*Formal Contract:*
- *Preconditions:* w ∈ T, w > 0
- *Definition:* actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})
- *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; wᵢ = 0 for all i < actionPoint(w); w_{actionPoint(w)} ≥ 1
