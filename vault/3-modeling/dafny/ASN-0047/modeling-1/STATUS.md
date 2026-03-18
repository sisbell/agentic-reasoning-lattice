# Verification Status — modeling-1

Updated: 2026-03-17 21:40
Verified: 33/33

| Property | Status | Divergences |
|----------|--------|-------------|
| EntitySetValid | verified |  |
| ProvenanceWellTyped | verified |  |
| IsInitialState | verified |  |
| ContentPermanence | verified |  |
| EntityPermanence | verified |  |
| EntityHierarchy | verified |  |
| ProvenancePermanence | verified |  |
| ArrangementMutability | verified | The ASN specifies multiset preservation of I-addresses under reordering (bijecti... |
| ContentAllocation | verified |  |
| ContentAllocatable | verified |  |
| EntityCreation | verified | The ASN states "When IsDocument(e): M'(e) = ∅" as an explicit postcondition. In ... |
| EntityCreatable | verified |  |
| ArrangementExtension | verified |  |
| ArrangementContraction | verified |  |
| ArrangementReordering | verified |  |
| ProvenanceRecording | verified |  |
| ProvenanceRecordable | verified |  |
| ArrangementInvariantsPreserved | verified | S2 (functionality) and S8-fin (finiteness) are structural in Dafny's map model —... |
| ValidComposite | verified | Elementary step predicates omit tumbler-level preconditions (IsElement for K.α, ... |
| PermanenceFromFrames | verified |  |
| ReachableStateInvariants | verified | S2 (injectivity) is structural — map<Tumbler, Tumbler> is a function. S8-fin is ... |
| AllocationRequiresPlacement | verified |  |
| ExtensionRecordsProvenance | verified |  |
| ProvenanceRequiresExtension | verified |  |
| HistoricalFidelity | verified |  |
| ContractionIsolation | verified |  |
| ReorderingIsolation | verified |  |
| ForkComposite | verified |  |
| ProvenanceBounds | verified | WF is an explicit precondition requiring arrangements exist only for allocated d... |
| DestructionConfinement | verified |  |
| ExistentialCoherence | verified |  |
| ProvenanceGrounding | verified |  |
| ProvenanceCoverage | verified |  |
