# ASN-0029 Proof Index

*Source: ASN-0029-document-ontology.md (revised 2026-03-11) — Index generated: 2026-03-11*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| AccountAddr | ValidAccountAddr | INV | predicate(Tumbler) | definition |
| account | HierarchicalParsing.AccountPrefix | INV | function(Tumbler): Tumbler | shared; in AddressAllocation |
| D0 | EmptyCreation | POST | ensures | includes pre and frame |
| D1 | DocumentAllocation | INV | predicate(DocId, DocId) | per-allocator |
| D2 | DocumentPermanence | INV | predicate(State, State) | transition |
| D3 | StructuralOwnership | INV | predicate(DocId) | state-independent |
| D4 | OwnershipPermanence | LEMMA | lemma | derived from D2, D3 |
| D5 | OwnershipRights | INV | predicate(State, DocId) | normative |
| D6 | IdentityByAddress | INV | predicate(DocId, DocId) | |
| D7 | OriginTraceability | INV | function(IAddr): DocId | definition |
| D7a | DocumentScopedAllocation | POST | ensures | INSERT postcondition |
| D7b | HomeDocumentMembership | LEMMA | lemma | derived from D7a, P2, D2 |
| D8 | InclusionNonDestruction | LEMMA | lemma | derived from P7 |
| D9 | EditIsolation | LEMMA | lemma | derived from P7 |
| Σ.pub | PublicationStatus | INV | State field | state extension |
| D10 | PublicationMonotonicity | INV | predicate(State, State) | transition |
| D10-ext | PublicationFrame | FRAME | ensures | for ASN-0026 ops |
| D10a | PublishOperation | POST | ensures | includes pre and frame |
| D11 | PublicationSurrender | INV | predicate(State, DocId) | normative |
| D12 | VersionCreation | POST | ensures | includes pre and frame |
| D13 | VersionPlacement | POST | ensures | D12 postcondition |
| D14 | VersionForest | INV | predicate(State) | includes parent membership |
| D14a | DocFieldWellFormed | INV | predicate(DocId) | |
| D15 | OwnerExclusiveModification | INV | predicate(State, DocId) | normative |
| D16 | NonOwnerForking | INV | predicate(State, DocId) | behavioral |
| D17 | ContentBasedDiscovery | POST | ensures | pure query; frame: Σ' = Σ |
