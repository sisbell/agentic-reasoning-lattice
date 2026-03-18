# ASN-0034 Proof Index

*Source: ASN-0034-tumbler-algebra.md (revised 2026-03-13) — Index generated: 2026-03-13*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|-------------|------|-----------|-------|
| T0(a) | UnboundedComponents | LEMMA | lemma | follows from carrier set definition |
| T0(b) | UnboundedLength | LEMMA | lemma | follows from carrier set definition |
| T1 | LexicographicOrder | INV | predicate(Tumbler, Tumbler) | defines total order |
| T2 | IntrinsicComparison | INV | predicate(Tumbler, Tumbler) | pure signature, no external state |
| T3 | CanonicalRepresentation | INV | predicate(Tumbler, Tumbler) | structural equality from datatype |
| T4 | ValidAddress | INV | predicate(Tumbler) | structural constraint on addresses |
| T5 | ContiguousSubtrees | LEMMA | lemma | derived from T1 |
| T6 | DecidableContainment | LEMMA | lemma | derived from T4; sub-parts (a)-(d) |
| T7 | SubspaceDisjoint | LEMMA | lemma | derived from T3, T4 |
| T8 | AllocationPermanence | INV | predicate(set<Tumbler>, set<Tumbler>) | transition |
| T9 | ForwardAllocation | INV | predicate(Tumbler, Tumbler) | per-allocator, transition |
| T10 | PartitionIndependence | LEMMA | lemma | derived from T3 |
| T10a | AllocatorDiscipline | INV | predicate(Tumbler, nat) | protocol constraint on inc usage |
| (Prefix ordering extension) | PrefixOrderingExtension | LEMMA | lemma | derived from T1 |
| (Partition monotonicity) | PartitionMonotonicity | LEMMA | lemma | derived from T1, T5, T9, T10, T10a, TA5 |
| (Global uniqueness) | GlobalUniqueness | LEMMA | lemma | derived from T3, T4, T9, T10, T10a, TA5 |
| TA0 | WellDefinedAddition | PRE | requires | w > 0, action point k ≤ #a |
| TA1 | AdditionWeakOrder | LEMMA | lemma | derived from ⊕ definition, T1 |
| TA1-strict | AdditionStrictOrder | LEMMA | lemma | derived from ⊕ definition, T1 |
| TA-strict | StrictIncrease | POST | ensures | on Add |
| TA2 | WellDefinedSubtraction | PRE | requires | a ≥ w |
| TA3 | SubtractionWeakOrder | LEMMA | lemma | derived from ⊖ definition, T1 |
| TA3-strict | SubtractionStrictOrder | LEMMA | lemma | derived from ⊖ definition, T1 |
| TA4 | PartialInverse | LEMMA | lemma | derived from ⊕, ⊖ definitions |
| (Reverse inverse) | ReverseInverse | LEMMA | lemma | derived from TA4, TA3-strict |
| TA5 | HierarchicalIncrement | POST | ensures | sub-conditions (a)-(d) on inc |
| (TA5 preserves T4) | IncrementPreservesValidity | LEMMA | lemma | derived from TA5, T4; k ≤ 2 |
| TA6 | ZeroTumblerSentinel | INV | predicate(Tumbler) | validity + ordering |
| TA7a | SubspaceClosure | LEMMA | lemma | derived from ⊕, ⊖ definitions |
| (Associativity) | AdditionAssociative | LEMMA | lemma | design does not depend on this |
| T12 | SpanWellDefined | INV | predicate(Tumbler, Tumbler) | non-emptiness from TA-strict |
