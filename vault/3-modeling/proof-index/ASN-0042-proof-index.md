# ASN-0042 Proof Index

*Source: ASN-0042-tumbler-ownership.md (revised 2026-03-15) — Index generated: 2026-03-16*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| O0 | StructuralOwnership | INV | predicate(Principal, Tumbler) | ownership decidable without state |
| O1 | PrefixDetermination | INV | predicate(Principal, Tumbler) | defines ownership predicate |
| O1a | AccountBoundary | INV | predicate(State) | |
| O1b | PrefixInjective | INV | predicate(State) | |
| O2 | OwnershipExclusivity | LEMMA | lemma | derived from O4, O1b |
| O3 | OwnershipRefinement | LEMMA | lemma | derived from O12, O13, T8; transition |
| O4 | DomainCoverage | LEMMA | lemma | derived from O5, O14, O16 |
| O5 | SubdivisionAuthority | INV | predicate(State, State) | transition |
| O6 | StructuralProvenance | LEMMA | lemma | derived from O1a, T4, AccountPrefix |
| O7 | OwnershipDelegation | POST | ensures | postconditions (a)(b)(c) of delegation |
| O8 | IrrevocableDelegation | LEMMA | lemma | derived from O3, O12, O13 |
| O9 | NodeLocalOwnership | LEMMA | lemma | derived from O1, O1a, T4 |
| O10 | DenialAsFork | POST | ensures | (a) ownership, (b) original unchanged |
| O11 | IdentityAxiomatic | INV | — | boundary axiom; authentication external |
| O12 | PrincipalPersistence | INV | predicate(State, State) | transition |
| O13 | PrefixImmutable | INV | predicate(State, State) | transition |
| O14 | BootstrapPrincipal | INV | predicate(State) | initial state |
| O15 | PrincipalClosure | INV | predicate(State, State) | transition |
| O16 | AllocationClosure | INV | predicate(State, State) | transition |
| O17 | AllocatedAddressValid | INV | predicate(State) | |
| AccountPrefix | AccountPrefix | LEMMA | lemma | derived from acct definition, T4 |
| Corollary | AccountPermanence | LEMMA | lemma | derived from O5, O14, O15 |
