# Cone Review — ASN-0034/TumblerSub (cycle 1)

*2026-04-15 12:54*

I'll read the ASN carefully, looking for cross-cutting issues between properties.

### `PositiveTumbler` referenced but undefined; `w > 0` is ambiguous between T1 ordering and the component-level predicate TumblerAdd actually requires

**Foundation**: T0 (CarrierSetDefinition), T1 (LexicographicOrder), T3 (CanonicalRepresentation)
**ASN**: TumblerAdd precondition — *"By PositiveTumbler, the precondition w > 0 means (E i : 1 ≤ i ≤ n : wᵢ ≠ 0)"*; D0 postcondition — *"b ⊖ a > 0"*; formal contracts of both properties use bare `w > 0`
**Issue**: TumblerAdd appeals to a property called `PositiveTumbler` to interpret `w > 0` as the component-level predicate `∃ i : wᵢ ≠ 0`. This property is never defined in the ASN. The formal contracts of both TumblerAdd and D0 use the notation `> 0` without disambiguation.

The notation is ambiguous because T has no unique zero element. By T3, the zero tumblers `[0]`, `[0,0]`, `[0,0,0]`, … are all distinct. Under T1, any zero tumbler of length ≥ 2 satisfies `w > [0]` via case (ii) — `[0]` is a proper prefix — yet has no nonzero component. So interpreting `w > 0` as a T1 comparison with any fixed zero tumbler does not yield the intended meaning. Concretely: `[0,0,0]` satisfies `[0,0,0] >_{T1} [0]`, but `{i : [0,0,0]_i ≠ 0} = ∅`, so the action point `min{i : wᵢ ≠ 0}` is undefined and TumblerAdd's construction fails at the first step.

The component-level predicate `∃ i : wᵢ ≠ 0` is strictly stronger than `w >_{T1} z` for any particular zero tumbler `z`, and it is the predicate TumblerAdd actually requires (the action point is the minimum of `{i : wᵢ ≠ 0}`, well-defined only when this set is non-empty). The gap is cross-cutting: every property that passes a displacement to TumblerAdd or reads one from D0 inherits the ambiguity in its precondition or postcondition chain.

**What needs resolving**: The ASN must define `PositiveTumbler` (or an equivalent) as an explicit property — either a predicate on T or a named subset — placed before TumblerAdd. The formal contracts of TumblerAdd and D0 should reference this defined predicate rather than the bare notation `w > 0`.
