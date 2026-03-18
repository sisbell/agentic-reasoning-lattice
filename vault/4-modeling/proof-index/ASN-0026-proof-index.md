# ASN-0026 Proof Index

*Source: ASN-0026-i-space-and-v-space.md (revised 2026-03-07) — Index generated: 2026-03-09*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| P0 | ISpaceImmutable | INV | predicate(State, State) | transition |
| P1 | ISpaceMonotone | INV | predicate(State, State) | transition |
| NO-REUSE | NoAddressReuse | LEMMA | lemma | derived from P0, P1 |
| P2 | ReferentiallyComplete | INV | predicate(State) | |
| P3 | MappingExact | INV | predicate(State) | architectural |
| P4 | CreationBasedIdentity | LEMMA | lemma | derived from ASN-0001 GlobalUniqueness |
| P5 | NonInjective | LEMMA | lemma | structural permission; existence witness |
| +_ext | ISpaceExtension | LEMMA | lemma | derived from P0, P1; transition form |
| P7 | CrossDocVIndependent | INV | predicate(State, State) | transition |
| P8 | NoRefCounting | LEMMA | lemma | derived from P1 |
| P9 (pre) | ValidInsertPos | PRE | requires | |
| P9 (length) | InsertLength | POST | ensures | |
| P9 (left) | LeftUnchanged | FRAME | ensures | |
| P9 (new) | FreshPositions | POST | ensures | |
| P9 (inj) | FreshInjective | POST | ensures | |
| P9 (right) | RightShifted | FRAME | ensures | |
| P11 | ViewerIndependent | INV | predicate(State) | architectural; enforced by function signature |
| REF-STABILITY | RefStability | LEMMA | lemma | derived from P7, P1, P2 |
