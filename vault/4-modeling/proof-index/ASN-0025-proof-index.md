# ASN-0025 Proof Index

*Source: ASN-0025-address-permanence.md (revised 2026-03-07) — Index generated: 2026-03-07*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| J0 | VSpaceGrounded | INV | predicate(State) | |
| J1 | TextContiguity | INV | predicate(State) | |
| J2 | LinkContiguity | INV | predicate(State) | |
| P0 | ISpaceGrowth | INV | predicate(State, State) | transition |
| P1 | ContentImmutability | INV | predicate(State, State) | transition |
| P2 | NoReuse | LEMMA | lemma | derived from P0, P1 |
| P6 | DocumentSetGrowth | INV | predicate(State, State) | transition |
| P3 | ISpaceNonExtension | FRAME | ensures | on Delete, Rearrange, Copy |
| UF | UniversalIFrame | FRAME | ensures | = P1 per-operation |
| UF-V | UniversalVFrame | FRAME | ensures | |
| P4 | RearrangementContentInvariance | POST | ensures | on Rearrange |
| Domain preservation | DomainPreservation | FRAME | ensures | on Rearrange |
| Exterior frame | ExteriorFrame | FRAME | ensures | on Rearrange |
| Link-subspace frame | LinkSubspaceFrame | FRAME | ensures | on Rearrange |
| P5 | TransclusionIdentity | POST | ensures | on Copy |
| P7 | CreationBasedIdentity | LEMMA | lemma | derived from T9, T10, GlobalUniqueness, P3 |
| P8 | ProvenanceNotLocation | INV | predicate(IAddr) | type-level property |
