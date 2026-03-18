# ASN-0036 Proof Index

*Source: ASN-0036-two-space.md (revised 2026-03-14) — Index generated: 2026-03-14*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| S0 | ContentImmutability | INV | predicate(State, State) | transition |
| S1 | StoreMonotonicity | LEMMA | lemma | derived from S0 |
| S2 | ArrangementFunctional | INV | predicate(State) | by construction (map type) |
| S3 | ReferentialIntegrity | INV | predicate(State) | |
| S4 | OriginBasedIdentity | LEMMA | lemma | derived from GlobalUniqueness (ASN-0034) |
| S5 | UnrestrictedSharing | LEMMA | lemma | derived from S0–S3; witness construction |
| S6 | PersistenceIndependence | LEMMA | lemma | derived from S0 |
| S7a | DocumentScopedAllocation | INV | predicate(State) | design requirement |
| S7b | ElementLevelAddresses | INV | predicate(State) | design requirement |
| S7 | StructuralAttribution | LEMMA | lemma | derived from S7a, S7b, T4 (ASN-0034) |
| S8-fin | FiniteArrangement | INV | predicate(State) | |
| S8a | VPositionWellFormed | INV | predicate(State) | |
| S8-depth | FixedDepthPositions | INV | predicate(State) | design requirement |
| S8 | SpanDecomposition | LEMMA | lemma | derived from S8-fin, S8a, S2, S8-depth |
| S9 | TwoSpaceSeparation | LEMMA | lemma | derived from S0 |
