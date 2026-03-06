# ASN-0001 Proof Index

*Source: ASN-0001-tumbler-algebra.md (revised 2026-02-23) — Index generated: 2026-03-01*

| ASN Label | Proof Label | Type | Construct | Notes |
|-----------|------------|------|-----------|-------|
| T0 | UnboundedComponents | INV | predicate(Tumbler) | axiom on carrier set |
| T1 | LexicographicOrder | INV | predicate(Tumbler, Tumbler) | defines total order |
| T2 | IntrinsicComparison | INV | predicate(Tumbler, Tumbler) | computability constraint; encoded by predicate signature |
| T3 | CanonicalRepresentation | INV | predicate(Tumbler, Tumbler) | equality criterion; automatic with Dafny datatypes |
| T4 | HierarchicalParsing | INV | predicate(Tumbler) | structural constraint on valid I-space addresses |
| T5 | ContiguousSubtrees | LEMMA | lemma | derived from T1 |
| T6 | DecidableContainment | LEMMA | lemma | corollary of T4 |
| T7 | SubspaceDisjointness | LEMMA | lemma | corollary of T3, T4 |
| T8 | AddressPermanence | INV | predicate(State, State) | transition |
| T9 | ForwardAllocation | INV | predicate(State, State) | transition |
| Prefix ordering extension | PrefixOrderingExtension | LEMMA | lemma | derived from T1 |
| Partition monotonicity | PartitionMonotonicity | LEMMA | lemma | derived from T9, T10, T1, T5 |
| T10 | PartitionIndependence | INV | predicate(Tumbler, Tumbler) | |
| T10a | AllocatorDiscipline | INV | predicate(State, State) | transition |
| Global uniqueness | GlobalUniqueness | LEMMA | lemma | derived from T9, T10, T10a |
| TA0 | WellDefinedAddition | PRE | requires | on Add; k ≤ #a |
| TA1 | WeakOrderPreservation | POST | ensures | algebraic law; a < b ⟹ a ⊕ w ≤ b ⊕ w |
| TA1-strict | StrictOrderPreservation | POST | ensures | algebraic law; requires k ≥ divergence(a, b) |
| TA-strict | StrictIncrease | POST | ensures | on Add; a ⊕ w > a |
| TA2 | WellDefinedSubtraction | PRE | requires | on Subtract; a ≥ w |
| TA3 | SubtractionPreservesOrder | POST | ensures | algebraic law; strict (<) unconditionally |
| TA4 | MutualInverse | POST | ensures | on Add/Subtract; requires k = #a, #w = k, zero prefix |
| Reverse inverse | ReverseInverse | LEMMA | lemma | derived from TA4, TA3 |
| TA5 | HierarchicalIncrement | POST | ensures | on Inc; sub-properties (a)–(d) |
| TA6 | ZeroTumblerInvalid | INV | predicate(Tumbler) | |
| TA7a | SubspaceClosure | POST | ensures | algebraic closure on Add/Subtract; element-local w |
| TA7b | SubspaceFrame | FRAME | ensures | on Insert/Delete |
| T11 | DualSpaceSeparation | INV | predicate(State, State) | transition; architectural |
| T12 | SpanWellDefined | INV | predicate(Tumbler, Tumbler) | non-emptiness from TA-strict |
| TA8 | OrthogonalDimensions | INV | predicate(Displacement) | 2D enfilade |
