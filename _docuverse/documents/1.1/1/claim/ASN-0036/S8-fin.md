**S8-fin (FiniteArrangement).** For each `d ∈ D`, `dom(Σ.M(d))` is finite in every reachable state `Σ`.

We establish the invariant by induction over the operation history.

*Base case.* By AX-1 (InitialEmptyState), `dom(Σ₀.M(d)) = ∅` for every document `d`. The empty set is finite.

*Inductive step.* Suppose `dom(Σ.M(d))` is finite in state Σ. Let Σ → Σ' be any state transition; by AX-5 (ClosedWorldTransition), some op ∈ Op produces Σ' from Σ. Each such operation acts on a finite selection of existing V-positions and introduces at most finitely many new ones — the union of a finite set with a finite set is finite, and the removal of elements from a finite set leaves a finite set. Therefore `dom(Σ'.M(d))` is finite.

This is a design requirement: every operation specification must individually discharge the obligation that it maps a finite arrangement to a finite arrangement. The base case and the closure argument above reduce that global invariant to a per-operation verification condition. ∎

*Formal Contract:*
- *Invariant:* dom(Σ.M(d)) is finite for every d ∈ D in every reachable state Σ
