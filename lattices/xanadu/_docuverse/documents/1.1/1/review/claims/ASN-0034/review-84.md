# Cone Review — ASN-0034/TumblerAdd (cycle 2)

*2026-04-16 12:23*

### ActionPoint formal contract omits the Depends field
**Foundation**: ActionPoint (this ASN)
**ASN**: ActionPoint section, Formal Contract block:
> *Formal Contract:*
> - *Preconditions:* w ∈ T, Pos(w)
> - *Definition:* actionPoint(w) = min({i : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0})
> - *Postconditions:* 1 ≤ actionPoint(w) ≤ #w; wᵢ = 0 for all i < actionPoint(w); w_{actionPoint(w)} ≥ 1

**Issue**: Every other property in this ASN (T0, T1, T3, PositiveTumbler, TumblerAdd) includes a *Depends* field enumerating the precise citations that license its preconditions, definition, and postconditions. ActionPoint's Formal Contract has no *Depends* entry even though its preconditions cite `Pos(·)` from PositiveTumbler and its carrier-set membership `w ∈ T` together with the length function `#w` and component projection `wᵢ` come from T0. The downstream consumer TumblerAdd correctly lists ActionPoint in its own Depends, but from ActionPoint's perspective the dependency chain to T0 and PositiveTumbler is not recorded. A formalizer scanning Depends fields to build the DAG will miss these edges and will not be able to verify that ActionPoint's proof of nonemptiness (which explicitly invokes PositiveTumbler: "Since Pos(w), PositiveTumbler guarantees at least one component of w is nonzero") is licensed by in-scope properties.

**What needs resolving**: ActionPoint's Formal Contract should carry a *Depends* field that records at minimum T0 (carrier set, length, component projection) and PositiveTumbler (the `Pos(w)` predicate that makes the `min`-set nonempty), matching the convention used by the other properties in the ASN.

## Result

Cone converged after 3 cycles.

*Elapsed: 903s*
