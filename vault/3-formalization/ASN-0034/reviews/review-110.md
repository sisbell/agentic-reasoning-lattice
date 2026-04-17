# Cone Review — ASN-0034/TA1 (cycle 1)

*2026-04-16 22:35*

### TA1 Depends omits T0, TA-Pos, and ActionPoint
**Foundation**: Internal — TA1 (OrderPreservationUnderAddition) within ASN-0034.
**ASN**: § Tumbler arithmetic, TA1 Formal Contract: `Depends: TA0 (WellDefinedAddition) … TumblerAdd … T1 … T3 …`.
**Issue**: TA1's Depends clause does not license three symbols/facts that the statement and proof invoke directly:
  1. **TA-Pos** — the precondition `Pos(w)` uses the positivity predicate defined in TA-Pos. TumblerAdd and TA0 cite TA-Pos whenever they state `Pos(w)`; TA1 does not.
  2. **ActionPoint** — the precondition `actionPoint(w) ≤ min(#a, #b)` uses the action-point function defined in ActionPoint. TumblerAdd and TA0 cite ActionPoint whenever they name `actionPoint`; TA1 does not.
  3. **T0 (CarrierSetDefinition)** — sub-case `j = k` asserts "addition of a fixed natural number preserves strict inequality on ℕ" to conclude `aₖ + wₖ < bₖ + wₖ`. The order-compatibility of `+` on ℕ is a T0 property. It is not a consequence of TA0, TumblerAdd, T1, or T3.

The neighbouring properties (TA0, TumblerAdd) cite T0, TA-Pos, and ActionPoint explicitly whenever they use those symbols or their order-on-ℕ facts, so the local convention is per-step citation, not transitive inheritance through TA0.
**What needs resolving**: Either extend TA1's Depends to include T0 (for ℕ-order-under-addition), TA-Pos (for `Pos`), and ActionPoint (for `actionPoint`) with the per-use rationales matching the established style, or state and defend a convention under which pass-through preconditions and ℕ-order facts need not be re-cited when already cited by a listed dependency.
