**TA-strict (StrictIncrease).** `(A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w > a)`.

TA-strict exports TumblerAdd's ordering postcondition as a single labelled fact so downstream users (chiefly T12 span well-definedness) can cite one corollary rather than TumblerAdd's full postcondition list.

*Proof.* Immediate from TumblerAdd's ordering-guarantee postcondition `a ⊕ w > a (T1)` under the preconditions `a, w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`, which are exactly TA-strict's hypotheses. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`
- *Depends:*
  - TumblerAdd (TumblerAdd) — ordering-guarantee postcondition `a ⊕ w > a (T1)` re-exported unchanged.
  - T0 (CarrierSetDefinition) — carrier `T` and length operator `#` in the quantifier range and precondition.
  - TA-Pos (PositiveTumbler) — precondition `Pos(w)`.
  - ActionPoint (ActionPoint) — precondition `actionPoint(w) ≤ #a`.
  - TA0 (WellDefinedAddition) — membership `a ⊕ w ∈ T` so T1's ordering applies to the left-hand side.
  - T1 (LexicographicOrder) — meaning of the strict ordering `>`.
- *Forward References:*
  - T12 (SpanWellDefinedness) — downstream user of this corollary; cites TA-strict for span well-definedness rather than TumblerAdd's full postcondition list.
- *Postconditions:* `a ⊕ w > a`
