# Triage — ASN-0034

*Generated: 2026-04-07 20:36*

## Promote

- T10a.1 → T10a.1 (UniformSiblingLength): referenced by GlobalUniqueness missing dep as "T10a Consequence 1"
- T10a.2 → T10a.2 (NonNestingSiblingPrefixes): independently citable; used by PartitionMonotonicity and SiblingPrefixNonNesting re-derivations
- T10a.3 → T10a.3 (LengthSeparation): independently citable; establishes parent-child allocator length separation
- T4b → T4b (UniqueParse): T6 missing dep cites T4(b) for fields(t) well-definedness
- T4c → T4c (LevelDetermination): T6 missing dep cites T4(c) for level computability from zeros(t)
- TA5a → TA5a (IncrementPreservesT4): T9 missing dep cites TA5(a) for inc strictness under T4

## Extract

(none)

## Leave

- DEF-DISPLACEMENT → DisplacementFromAToB: notation for w = b ⊖ a, internal to D0
- ZEROS-COUNT → ZeroCount: redundant re-definition of T4's zeros(t) across GlobalUniqueness, T4, T6
- OrdinalDisplacementNotation → OrdinalDisplacementShorthand: shorthand δₙ for existing OrdinalDisplacement property
- D-SPAN → SpanPair: T12's own definition (dedup D-SPAN = D-Span)
- D-FieldSeparator → FieldSeparator: T4's own definition (dedup unnamed = D-FieldSeparator)
- D-FieldExtraction → FieldsExtraction: T4's own definition; re-definitions in T6 (D-FieldDecomposition) are redundant (dedup of 6 findings)
- ZERO-TUMBLER → ZeroTumbler: complementary definition within PositiveTumbler, not cross-referenced
- DA0 → ActionPoint: TA0's own definition (dedup DA0 = DEF-ActionPoint)
- DA-TumblerAdd → TumblerAdd: re-definition in TA0 of property that has its own file
- DEF-TA2-SUB → TumblerSubtraction: TA2's own ⊖ notation (dedup of 2)
- TD-ZPE → ZeroPaddedEquality: internal relation for TA3 proof only (dedup TD-ZPE = DEF-ZeroPaddedEquality)
- DA-SIG → LastSignificantPosition: TA5's own sig(t) definition (dedup DA-SIG = D-SigPos)
- TD-S → SubspaceOrdinalSet: TA7a's own domain set S (dedup TD-S = TA7-S)
- D-GhostElement → GhostElement: T8's own concept, not cross-referenced in other contracts
- OrdShiftDepth → ShiftDepthPreservation: sub-lemma within OrdinalShift proof (dedup of 3 findings)
- OrdShiftStability → ShiftHeadPreservation: sub-lemma within OrdinalShift proof (dedup of 3 findings)
- OrdShiftPositivity → ShiftComponentPositivity: sub-lemma within OrdinalShift proof (dedup of 2 findings)
- SIBLING-PREFIX-NON-NESTING → SiblingPrefixNonNesting: re-derives T10a.2 within PartitionMonotonicity (dedup of 2)
- PREFIX-ORDERING-EXTENSION → PrefixOrderingExtension: already exists in property table as standalone
- POSITIVE-ABOVE-ZERO → PositiveDominatesZero: re-verifies TA6 (dedup of 3 findings)
- T0a → UnboundedComponentValues: already exists in property table as T0(a)
- T10a-N → AllocatorDisciplineNecessity: necessity/counterexample argument, not a positive result
- T4a → SyntacticEquivalence: sub-result characterizing T4, not cross-referenced
- T7a → TextPrecedesLinksInOrder: sub-result of T7, not cross-referenced
- T9c → GrowingAllocatedSet: consequence of T8+T9, not cross-referenced (dedup T9c = T9a)
- TA1 → AddWeakMonotonicity: re-verifies existing TA1 property (dedup with TA1S)
- TA1-strict → AddStrictMonotonicity: re-verifies existing TA1-strict property
- TA3 → SubtractWeakMonotonicity: re-verifies existing TA3 property (dedup with TA3S)
- TA3-strict → SubtractStrictMonotonicity: re-verifies existing TA3-strict property
- TA4 → AddSubtractRoundTrip: re-verifies existing TA4 property
- TA-RC-GEN → TailErasureCorollary: re-verifies existing TA-MTO property
- TA-noncomm → AdditionNonCommutative: structural observation within TA-assoc, not cross-referenced
- TA-apmin → ActionPointComposition: internal lemma of TA-assoc proof
- TA5-SigValid → SigOnValidAddresses: sub-result within TA5, follows trivially from T4
- TA7b → SubspaceClosureSMembership: extension result within TA7a, not cross-referenced
- TA-RESULT-LENGTH → ResultLengthIdentity: re-states TumblerAdd definition's length clause (dedup of 2)
- TUMBLER-ADD-MANY-TO-ONE → TumblerAddManyToOne: re-verifies existing TA-MTO property
- _zero-extension-is-immediate-successor → ZeroExtensionIsImmediateSuccessor: structural result, not cross-referenced
