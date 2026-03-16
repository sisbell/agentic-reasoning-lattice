# ASN-0040 Proof Index

*Source: ASN-0040-tumbler-baptism.md (revised 2026-03-15) — Index generated: 2026-03-16*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| S0 | StreamStrictlyOrdered | LEMMA | lemma | derived from TA5(a) |
| S1 | StreamExtendsParent | LEMMA | lemma | derived from TA5(b) |
| B0 | Irrevocability | INV | predicate(State, State) | transition |
| B0a | BaptismalClosure | INV | predicate(State, State) | transition |
| B₀ conf. | SeedConformance | INV | predicate(set\<Tumbler\>) | initial state |
| B1 | ContiguousPrefix | INV | predicate(State) | |
| B2 | HighWaterMarkSufficiency | LEMMA | lemma | derived from B1 |
| B3 | GhostValidity | INV | predicate(State) | downstream req on content ops |
| B4 | NamespaceSerialized | PRE | requires | on baptize |
| B5 | FieldAdvancement | LEMMA | lemma | derived from TA5 |
| B5a | SiblingZerosPreserved | LEMMA | lemma | derived from TA5(c) |
| B6 | ValidDepth | PRE | requires | on baptize |
| B7 | NamespaceDisjointness | LEMMA | lemma | derived from T3, T4, T10 |
| B8 | GlobalUniqueness | LEMMA | lemma | derived from B1, B4, B7 |
| B9 | UnboundedExtent | LEMMA | lemma | derived from T0(a), B1 |
| B10 | RegistryT4Validity | LEMMA | lemma | derived from B₀ conf., B6 |
| Bop (POST) | RegistryGrowth | POST | ensures | on baptize |
| Bop (FRAME) | OnlyRegistryModified | FRAME | ensures | on baptize |
