## Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`. The two predicates are DeMorgan duals: `Zero(t) ⟺ ¬Pos(t)` holds unconditionally. `Zero(t)` is stated with its universal as the defining clause rather than as `¬Pos(t)` so that downstream consumers can read `zᵢ = 0` off the definition directly without routing through a negated existential.

We additionally introduce the set-form **Z** = {t ∈ T : Zero(t)}, the reification of `Zero` on T, so that `t ∈ Z ⟺ Zero(t)`. `Z` is derived notation, not a new primitive.

The predicate `Pos(t)` is not written `t > 0`, because `>` already denotes T1's lexicographic ordering, and the two notions diverge. The all-zero tumbler `[0, 0]` exhibits the divergence: under T1, `[0] < [0, 0]` by the prefix rule, yet `Zero([0, 0])` holds. The converse direction — `Pos(t)` implies `t` is T1-greater than every zero tumbler — does hold, but its proof consumes ActionPoint and T1, and is established separately.

*Formal Contract:*
- *Definition:* `Pos(t)` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `Zero(t)` iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`; **Z** = {t ∈ T : Zero(t)}.
- *Depends:* T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`.
