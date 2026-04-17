# Cone Review — ASN-0034/TumblerAdd (cycle 1)

*2026-04-16 19:36*

### `PositiveTumbler`'s Formal Contract Depends list omits T0
**Foundation**: `T0 (CarrierSetDefinition)` — supplies the carrier set `T`, the length operator `#·`, the component projection `·ᵢ`, and the ℕ properties (notably that a nonzero natural number is `≥ 1`).
**ASN**: `PositiveTumbler` Formal Contract:
> *Depends:* T1 (LexicographicOrder) — the postcondition proof invokes T1 case (i) ... TA0 (WellDefinedAddition) [forward reference — ...] — the closing prose paragraph cites TA0's precondition `Pos(w)` ...

The Definition itself reads "`Pos(t)` (positive) iff `(E i : 1 ≤ i ≤ #t : tᵢ ≠ 0)`" and the proof argues "`zₖ = 0 < tₖ` because `tₖ ≥ 1` as a nonzero natural number".
**Issue**: PositiveTumbler's Definition uses `t ∈ T`, `#t`, and `tᵢ`, all introduced by T0. Its postcondition proof additionally relies on T0's ℕ properties — the step `tₖ ≥ 1 as a nonzero natural number` is licensed by T0's discreteness axiom (no `m ∈ ℕ` with `0 < m < 1`). Yet the Depends list cites only T1 and TA0; T0 is absent. This is exactly the kind of gap that the cycle-2 finding fixed for ActionPoint, where T0 was added to the Depends because the predicate `Pos(w)`, length `#w`, and component projection `wᵢ` came from T0. PositiveTumbler is one level closer to T0 (it *defines* `Pos`) and has the same dependency, but its contract does not record it. A formalizer or downstream pipeline that builds the dependency DAG from Depends fields will fail to register the PositiveTumbler→T0 edge, and will not be able to discharge the "nonzero natural ⇒ ≥ 1" step in the postcondition proof from in-scope axioms.
**What needs resolving**: PositiveTumbler's Formal Contract should add T0 to its *Depends* field, citing T0 for (i) the carrier set, length, and component-projection notation used in the Definition and the zero-tumbler companion definition, and (ii) the ℕ property "nonzero ⇒ `≥ 1`" used in the postcondition proof. The annotation should match the convention now used by ActionPoint.
