**TA5-SIG (LastSignificantPosition).** We define the *last significant position* of a tumbler `t ∈ T`, written `sig(t)`.

When `t` has at least one nonzero component — that is, `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` — we set `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`, the position of the rightmost nonzero component.

When every component of `t` is zero — that is, `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` — we set `sig(t) = #t`.

In both cases `1 ≤ sig(t) ≤ #t`, since `#t ≥ 1` for every `t ∈ T`.

*Formal Contract:*
- *Preconditions:* `t ∈ T` (any tumbler with `#t ≥ 1`).
- *Definition:* `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `sig(t) = #t` when `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies `t ∈ T` as finite ℕ-sequences with `#t ≥ 1`, component projection `tᵢ`, and the length `#t` used as the fallback value and index bound.
  - NAT-wellorder (NatWellOrdering) — greatest-element principle (dual of least-element) gives `max` on the nonempty subset `{i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}` of ℕ bounded above by `#t`.
- *Postconditions:* `1 ≤ sig(t) ≤ #t`.
