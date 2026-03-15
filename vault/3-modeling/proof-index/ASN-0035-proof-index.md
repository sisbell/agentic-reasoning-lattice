# ASN-0035 Proof Index

*Source: ASN-0035-node-ontology.md (revised 2026-03-14) — Index generated: 2026-03-14*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| Σ.nodes | BaptizedNodes | INV | predicate(State) | state component |
| N0 | GhostElement | LEMMA | lemma | derived from T12 |
| N1 | IdentityByAssignment | INV | predicate(Tumbler) | |
| N2 | SingleRoot | INV | predicate(State) | |
| N3 | NodeTree | INV | predicate(State) | |
| N4 | BaptismMonotonicity | INV | predicate(State, State) | transition |
| N5 | SequentialChildren | INV | predicate(State) | |
| N6 | StructuralOrdering | LEMMA | lemma | derived from N3, N5, T1 |
| N7 | ForwardReferenceAdmissibility | LEMMA | lemma | derived from T12 |
| N8 | AlwaysValidStates | LEMMA | lemma | derived from N2–N6 preservation |
| N9 | SubtreeContiguity | LEMMA | lemma | derived from T5 |
| N10 | SubtreeDisjointness | LEMMA | lemma | derived from T10 |
| N11 | CoordinationFreeDisjointness | LEMMA | lemma | derived from GlobalUniqueness (ASN-0034) |
| N12 | LocalSerializationSufficiency | LEMMA | lemma | derived from BAPTIZE, N10 |
| N13 | UniformNodeType | INV | predicate(Tumbler) | |
| N14 | NoNodeMutableState | INV | predicate(Tumbler) | |
| N15 | AllocationAuthority | PRE | requires | BAPTIZE precondition |
| DC1 | AuthorityPermanence | INV | predicate(State, State) | design constraint; transition |
| N16 | PrefixPropagation | LEMMA | lemma | derived from TA5 |
