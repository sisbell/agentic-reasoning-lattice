# Review of ASN-0047

Based on Dafny verification — 33 properties, 27 clean, 6 with divergences

## REVISE

No genuine spec issues found. All divergences are encoding artifacts.

## QUALITY

### File: ArrangementContraction.dfy — SIMPLIFY

Six trivial decomposition lemmas (ContractionStrictlyShrinks, ContractionPreservesMappings, FrameOtherDocuments, FrameEntities, FrameContent, FrameProvenance) — all empty bodies, all restating individual conjuncts of `Post`. No module imports ArrangementContraction, so these lemmas are unused.

Remove all six. The `Post` predicate is the API; callers can destructure it directly.

### File: ArrangementExtension.dfy — SIMPLIFY

Seven trivial decomposition lemmas — same pattern as ArrangementContraction. All empty bodies, all unused. Remove them.

### File: ProvenanceRecording.dfy — SIMPLIFY

Six trivial decomposition lemmas (RecordingAddsEntry, RecordingPreservesExisting, RecordingExactGrowth, RecordingFrameContent, RecordingFrameEntities, RecordingFrameMapping). All empty bodies, restating conjuncts of `Post`. No external imports. Remove them.

### File: ContentAllocation.dfy — SIMPLIFY

Three trivial decomposition lemmas (AllocationMapsCorrectly, AllocationPreservesExisting, AllocationExtendsDomain). All empty bodies, all unused. Marginal — fewer than the other files — but still pure restatement of `Post` with no callers.

### File: AllocationRequiresPlacement.dfy — PASS
### File: ArrangementInvariantsPreserved.dfy — PASS
### File: ArrangementMutability.dfy — PASS
### File: ArrangementReordering.dfy — PASS
### File: ContentAllocatable.dfy — PASS
### File: ContentPermanence.dfy — PASS
### File: ContractionIsolation.dfy — PASS
### File: DestructionConfinement.dfy — PASS
### File: EntityCreatable.dfy — PASS
### File: EntityCreation.dfy — PASS
### File: EntityHierarchy.dfy — PASS
### File: EntityPermanence.dfy — PASS
### File: EntitySetValid.dfy — PASS
### File: ExistentialCoherence.dfy — PASS
### File: ExtensionRecordsProvenance.dfy — PASS
### File: ForkComposite.dfy — PASS
### File: HistoricalFidelity.dfy — PASS
### File: IsInitialState.dfy — PASS
### File: PermanenceFromFrames.dfy — PASS
### File: ProvenanceBounds.dfy — PASS
### File: ProvenanceCoverage.dfy — PASS
### File: ProvenanceGrounding.dfy — PASS
### File: ProvenancePermanence.dfy — PASS
### File: ProvenanceRecordable.dfy — PASS
### File: ProvenanceRequiresExtension.dfy — PASS
### File: ProvenanceWellTyped.dfy — PASS
### File: ReachableStateInvariants.dfy — PASS
### File: ReorderingIsolation.dfy — PASS
### File: ValidComposite.dfy — PASS

## SKIP

### Dafny map model gives S2 and S8-fin structurally

ArrangementInvariantsPreserved (line 23) and ReachableStateInvariants (line 11) both note that `map<Tumbler, Tumbler>` is inherently functional (S2) and finite (S8-fin). These are properties the ASN must state — they are non-trivial in the mathematical domain — but Dafny's type system satisfies them by construction. S8a/S8-depth are abstracted into VPosValid in ArrangementInvariantsPreserved, which is the correct encoding.

### Reordering bijection scoped to ArrangementReordering, not ArrangementMutability

ArrangementMutability (line 72) notes that its IsArrReorder predicate captures only frame conditions, not multiset preservation. This is deliberate scope limitation — P3 needs only monotonicity of C/E/R, which the frame conditions provide. The full bijection model lives in ArrangementReordering.dfy where it belongs.

### Entity creation empty arrangement follows from map convention

EntityCreation (line 33): the ASN's "When IsDocument(e): M'(e) = ∅" is an explicit postcondition; in Dafny, M is in frame (unchanged) and absence from the map represents ∅. The NewDocumentEmpty lemma captures this correctly under the well-formedness assumption. No spec ambiguity.

### Partial-map WF precondition in ProvenanceBounds

ProvenanceBounds (line 33): the ASN defines M as total with M(d) = ∅ for d ∉ E_doc. Dafny's partial-map model requires an explicit WF predicate to link arrangement entries back to E_doc membership. This is a representation gap, not a spec gap. The totality convention is well-defined in the ASN.

### ProvDocValid as explicit invariant

ReachableStateInvariants (line 90): R ⊆ T_elem × E_doc is a type constraint in the ASN. Dafny can't express this as a type, so it becomes an explicit invariant. K.ρ's precondition (d ∈ E_doc) plus P1 maintain it inductively. The ASN's structural typing is correct.

### Composite as conjuncts vs derived from elementary frames

ReachableStateInvariants (line 121): the Composite predicate states permanence, coupling, and per-state invariants as conjuncts rather than deriving them from modular lemmas. This is a proof-structuring choice — the ASN's derivation chain (PermanenceFromFrames, ArrangementInvariantsPreserved, etc.) is correct; the Dafny proof just inlines the conclusions.

### Elementary steps omit tumbler-level preconditions

ValidComposite (line 33): K.α omits IsElement(a) and K.δ omits parent(e) ∈ E from the Step predicate. These are modeled separately in ContentAllocatable and EntityCreatable. Orthogonal decomposition — the coupling analysis doesn't depend on address-level constraints.

VERDICT: SIMPLIFY
