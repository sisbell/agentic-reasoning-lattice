**TA5-SIG (LastSignificantPosition).** We define the *last significant position* of a tumbler `t ∈ T`, written `sig(t)`.

When `t` has at least one nonzero component — that is, `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` — we set `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})`, the position of the rightmost nonzero component.

When every component of `t` is zero — that is, `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` — we set `sig(t) = #t`.

In both cases `1 ≤ sig(t) ≤ #t`, since `#t ≥ 1` for every `t ∈ T`.

*Formal Contract:*
- *Preconditions:* `t ∈ T` (any tumbler with `#t ≥ 1`).
- *Definition:* `sig(t) = max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` when `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `sig(t) = #t` when `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.
- *Depends:* T0 (CarrierSetDefinition) — the precondition `t ∈ T`, the length `#t` together with the guarantee `#t ≥ 1` that makes the fallback branch's value `sig(t) = #t` a well-defined index in `{1, ..., #t}`, and the component projection `tᵢ` used in the case predicates `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)` and `(A i : 1 ≤ i ≤ #t : tᵢ = 0)` all come from T0's characterisation of T as finite sequences over ℕ with length ≥ 1; the ℕ-valued components that T0 supplies are what make the test `tᵢ ≠ 0` well-formed as a predicate on the carrier. NAT-wellorder (NatWellOrdering) — the definition's `max({i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0})` step invokes the dual of NAT-wellorder's least-element principle: the set `{i : 1 ≤ i ≤ #t ∧ tᵢ ≠ 0}` is a nonempty (by the case hypothesis `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`) subset of ℕ bounded above by `#t` (a subset of ℕ because indices `i` with `1 ≤ i ≤ #t` lie in ℕ, bounded because every member satisfies `i ≤ #t`), and the greatest-element principle for nonempty bounded subsets of ℕ — the standard dual of NAT-wellorder's least-element principle, obtained by applying the least-element principle to the reflected set `{#t - i + 1 : i ∈ S}` — supplies the maximum that `max` names, so the well-definedness of `max(·)` is discharged from NAT-wellorder rather than left as an implicit appeal, matching the convention ActionPoint and Divergence follow when they cite NAT-wellorder for `min(·)`.
- *Postconditions:* `1 ≤ sig(t) ≤ #t`.
