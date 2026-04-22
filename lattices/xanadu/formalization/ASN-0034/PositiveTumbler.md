## Zero tumblers and positivity

**TA-Pos (PositiveTumbler).** A tumbler `t ∈ T` is *positive*, written `Pos(t)`, iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`. A tumbler `t ∈ T` is a *zero tumbler*, written `Zero(t)`, iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`.

The set of zero tumblers is written **Z** = {t ∈ T : Zero(t)}.

The predicate `Pos(t)` is not written `t > 0`, because `>` already denotes T1's lexicographic ordering, and the two notions diverge. The zero tumbler `0.0.0` exhibits the divergence: under T1, `0.0 < 0.0.0` by the prefix rule (the length-2 tumbler `0.0` is a proper prefix of the length-3 tumbler `0.0.0`), yet `Zero(0.0.0)` holds.

*Formal Contract:*
- *Definition:* `Pos(t)` iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`; `Zero(t)` iff `(A i : 1 ≤ i ≤ #t : tᵢ = 0)`; **Z** = {t ∈ T : Zero(t)}.
- *Depends:*
  - T0 (CarrierSetDefinition) — carrier `T`, length `#t`, component projection `tᵢ`.
  - T1 (LexicographicOrder) — reserves `<` (hence `>`) for lexicographic order and supplies the prefix rule, both invoked to exhibit the divergence between `Pos` and `> 0`.
