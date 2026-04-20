## Definition (Span)

**Definition (Span).** A *span* is the address-set `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}` determined by a pair `(s, ℓ)` where `s ∈ T` is a start address and `ℓ ∈ T` is a length — a positive tumbler used as a displacement whose action point satisfies `actionPoint(ℓ) ≤ #s`.

*Formal Contract:*
- *Preconditions:* `s ∈ T`, `ℓ ∈ T`, `Pos(ℓ)`, `actionPoint(ℓ) ≤ #s`
- *Definition:* `span(s, ℓ) = {t ∈ T : s ≤ t < s ⊕ ℓ}`
- *Depends:*
  - T0 (CarrierSetDefinition) — supplies the carrier `T` and length operator `#`.
  - TA-Pos (PositiveTumbler) — supplies the positivity predicate `Pos(·)`.
  - ActionPoint (ActionPoint) — supplies the action-point function `actionPoint(·)`.
  - TumblerAdd (TumblerAdd) — supplies the operator `⊕`.
  - TA0 (WellDefinedAddition) — licenses `s ⊕ ℓ ∈ T` under the four preconditions via the instantiation `(a, w) := (s, ℓ)`.
  - T1 (LexicographicOrder) — supplies the strict order `<` and the non-strict `≤` bracketing the defining set.
