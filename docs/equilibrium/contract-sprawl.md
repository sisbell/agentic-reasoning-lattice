# Contract Sprawl

A property's formal contract keeps growing across review cycles. Each new clause invalidates the completeness of every existing citation. Reviews keep finding citation gaps created by the previous cycle's extension. The contract never stops moving.

## Cause: Genesis Attractor

The property at the genesis of a concept — the first property in the ASN that introduces it — becomes the default home for every fact anyone needs about that concept. Downstream reasoning has nowhere else to put new facts.

## Signal

The same property's contract grows across multiple review cycles.

## Example: T0 absorbing ℕ

![Contract sprawl: genesis attractor and resolution](../diagrams/contract-sprawl.svg)

ASN-0034's T0 (CarrierSetDefinition) started as "T = finite sequences over ℕ; ℕ with standard properties." Over three different cones and four cycles, T0's contract grew to state: additive identity, strict total order (irreflexivity, transitivity, trichotomy), discreteness, order compatibility, successor inequality, and well-ordering.

Sources:
- D0 cone added discreteness for ZPD's proof
- TumblerAdd cone added ordering axioms for T1's trichotomy
- TumblerAdd cone added additive axioms for action-point arithmetic
- TumblerAdd cone added well-ordering for T10's `min` operation

During the same period, TumblerAdd and T10a-N cones both hit cycle 8 without converging. Both had remaining findings about T0 citation completeness.

T0 was the only property introducing ℕ. Every ℕ fact had nowhere else to go.

## Resolution

**Split the attractor into dedicated properties.** T0 becomes T0 (carrier set) plus NAT-wellorder, NAT-discrete, NAT-order, NAT-addcompat, etc. Each independently citable.

With the split, new facts about the concept are added as new properties, not as clauses to an existing one. Previous citations stay valid because no existing contract changes. Growth is by accretion instead of mutation. The attractor is dissolved — no single property is the sole home for the concept, so there is no accumulation point.

**Follow the split with [review/revise iteration](../patterns/review-revise-iteration.md).** The split leaves downstream citations pointing at the old attractor for facts that moved. Review/revise realigns them.

## Related

- [Accretion](../patterns/accretion.md) — the pattern that prevents Contract Sprawl. Properties grow by adding new properties, not by mutating existing ones.
- [Dependency cone](../patterns/dependency-cone.md) — can mask Contract Sprawl. A non-converging cone may look like coupling when the real cause is an apex sprawling each cycle.
- [Review V-Cycle](../design-notes/review-v-cycle.md) — clean full-review followed by cones finding issues often traces back to a Genesis Attractor.