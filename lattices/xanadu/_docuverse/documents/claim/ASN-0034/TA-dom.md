**TA-dom (DisplacementDominance).** `(A a, w ∈ T : Pos(w) ∧ actionPoint(w) ≤ #a : a ⊕ w ≥ w)`.

TA-dom exports TumblerAdd's fourth postcondition — `a ⊕ w ≥ w (T1, T3)` — as a single labelled corollary for downstream use.

*Proof.* Immediate from TumblerAdd's *dominance guarantee* postcondition `a ⊕ w ≥ w (T1, T3)` under the preconditions `a, w ∈ T`, `Pos(w)`, `actionPoint(w) ≤ #a`, which are exactly TA-dom's hypotheses. ∎

*Formal Contract:*
- *Preconditions:* `a ∈ T`, `w ∈ T`, `Pos(w)`, `k ≤ #a` where `k` is the action point of `w`
- *Depends:*
  - TumblerAdd — sole arithmetic source; exports `a ⊕ w ≥ w (T1, T3)` as its fourth postcondition.
  - TA-Pos (PositiveTumbler) — licenses `Pos(w)` precondition and the existence of the action point.
  - ActionPoint — licenses `actionPoint(w) ≤ #a` precondition.
  - TA0 (WellDefinedAddition) — supplies `a ⊕ w ∈ T` (so T1's ordering applies on the left) and `#(a ⊕ w) = #w` (consumed by T3 in the equality case).
  - T1 (LexicographicOrder) — meaning of `≥` via `a ≥ b ⟺ b ≤ a` and `a ≤ b ⟺ a < b ∨ a = b`.
  - T3 (CanonicalRepresentation) — equality-from-component-agreement-and-equal-length, used when `aᵢ = 0` for all `i ≤ k`.
- *Postconditions:* `a ⊕ w ≥ w`
