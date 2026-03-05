# ASN-0004 Property Contract

*Source: ASN-0004-content-insertion.md (revised 2026-02-24) — Contract generated: 2026-03-01*

| ASN Label | Dafny Name | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| S-DISJ | SubspaceDisjoint | INV | predicate(State) | |
| S0 | VIGrounding | INV | predicate(State) | |
| S1 | IspaceImmutable | INV | predicate(State, State) | transition |
| S2 | LinkGrounding | INV | predicate(State) | |
| S3 | SpanIndexConsistent | INV | predicate(State) | |
| S4 | PoomInjective | INV | predicate(State) | |
| S5 | PositionsDense | INV | predicate(State) | |
| P0 | AddressIrrevocable | LEMMA | lemma | derived from S1 |
| P1 | ContentImmutable | LEMMA | lemma | restates S1 |
| P2 | SpanIndexMonotone | INV | predicate(State, State) | transition; axiom |
| PRE1 | DocExists | PRE | requires | |
| PRE2 | IsOwner | PRE | requires | |
| PRE3 | PositionValid | PRE | requires | |
| PRE4 | ContentNonEmpty | PRE | requires | |
| INS1 | FreshAddresses | POST | ensures | |
| INS1a | TextSubspaceAllocation | POST | ensures | |
| INS2 | ContentEstablished | POST | ensures | |
| INS3 | ContentPlacement | POST | ensures | |
| INS4 | PositionShift | POST | ensures | |
| INS-D1 | DomainSize | LEMMA | lemma | derived from INS3, INS4 |
| INS5 | SpanIndexExtended | POST | ensures | |
| INS-F1 | IspaceUpperBound | FRAME | ensures | |
| INS-F2 | OtherDocsUnchanged | FRAME | ensures | |
| INS-D2 | VICorrespondencePreserved | LEMMA | lemma | derived from INS4, P1 |
| INS-F4 | LinksPreserved | FRAME | ensures | |
| INS-F4a | NoNewLinks | FRAME | ensures | |
| INS-F5 | SubspaceIsolation | FRAME | ensures | |
| INS-F6 | SpanIndexUpperBound | FRAME | ensures | |
| INS-CORR | InsertCorrectness | LEMMA | lemma | derived from P0, P1, P2, INS1–INS5, INS-F1–INS-F6 |
| INS-ATOM | InsertAtomic | LEMMA | lemma | inherent in functional model |
