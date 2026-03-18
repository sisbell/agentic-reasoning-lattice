# ASN-0043 Proof Index

*Source: ASN-0043-link-ontology.md (revised 2026-03-16) — Index generated: 2026-03-17*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| Σ.L | LinkStore | DEF | State field | `T ⇀ Link` |
| Endset | Endset | DEF | type | `set<Span>` |
| Link | Link | DEF | datatype | `(from: Endset, to: Endset, typ: Endset)` |
| home(a) | Home | DEF | function | `= Origin(a)` for link addresses |
| coverage(e) | Coverage | DEF | function | union of span address sets |
| L0 | SubspacePartition | INV | predicate(State) | |
| L1 | LinkElementLevel | INV | predicate(State) | |
| L1a | LinkScopedAllocation | INV | predicate(State) | |
| L2 | OwnershipEndsetIndependence | LEMMA | lemma | derived from L1, L1a, T4 |
| L3 | TripleEndsetStructure | INV | datatype Link | encoded in type definition |
| L4 | EndsetGenerality | INV | predicate(State) | only T12 constrains spans |
| L5 | EndsetSetSemantics | INV | type Endset | encoded in set type |
| L6 | SlotDistinction | INV | predicate(Link) | follows from datatype equality |
| L7 | DirectionalFlexibility | META | — | meta-property of L0–L14 |
| L8 | TypeByAddress | INV | predicate(State) | |
| L9 | TypeGhostPermission | LEMMA | lemma | existence proof; witness construction |
| L10 | TypeHierarchyByContainment | LEMMA | lemma | derived from T1, T5 |
| L11 | IdentityByAddress | INV | predicate(State) | |
| L12 | LinkImmutability | INV | predicate(State, State) | transition |
| L12a | LinkStoreMonotonicity | LEMMA | lemma | derived from L12; transition |
| L13 | ReflexiveAddressing | LEMMA | lemma | derived from L1, T1, T12 |
| L14 | DualPrimitive | INV | predicate(State) | |
