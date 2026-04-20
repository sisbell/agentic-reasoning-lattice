# Review of ASN-0036

Based on Dafny verification — 15 properties, 15 verified, 2 divergences reported

## REVISE

No genuine spec issues found.

## QUALITY

### File: ArrangementFunctional.dfy — PASS
### File: ContentImmutability.dfy — PASS
### File: DocumentScopedAllocation.dfy — PASS
### File: ElementLevelAddresses.dfy — PASS
### File: FiniteArrangement.dfy — PASS
### File: FixedDepthPositions.dfy — PASS
### File: OriginBasedIdentity.dfy — PASS
### File: PersistenceIndependence.dfy — PASS
### File: ReferentialIntegrity.dfy — PASS
### File: SpanDecomposition.dfy — PASS

Well-structured proof. The three helper lemmas (`OrdinalOffsetZero`, `SingletonRunValid`, `SingletonInRunIdentity`) each serve a distinct role in the decomposition argument. The main lemma body has clean separation of the three proof obligations (validity, coverage, uniqueness).

### File: StoreMonotonicity.dfy — PASS
### File: StructuralAttribution.dfy — PASS

`ZeroCountFindZero` is a necessary inductive lemma for navigating the component sequence. `ElementLevelHasElementField` bridges the zero-count characterization to the field-extraction API. Both are load-bearing.

### File: TwoSpaceSeparation.dfy — PASS
### File: UnrestrictedSharing.dfy — PASS

`WitnessArrangement` is a good abstraction — the recursive construction is cleaner than inline map literals and the ensures clauses carry the proof obligations.

### File: VPositionWellFormed.dfy — PASS

## SKIP

### Proof artifacts: DocumentScopedAllocation and StructuralAttribution divergences

Both divergences concern the same gap: the ASN's S7a and S7 make *causal* claims about allocation provenance ("the document whose owner performed the allocation," "uniquely identifies the allocating document"). These are system-level invariants about the allocation protocol (T9, T10 from ASN-0034) — they describe who performed an action, not what the resulting state looks like.

Dafny can express the *structural consequence*: every stored address has an element field, its document-level prefix belongs to the known document set, and the origin is a well-defined prefix of the address. It cannot express the causal claim that this prefix identifies the allocator rather than merely being a structural artifact.

The ASN already handles this correctly. S7a is explicitly labeled a "design requirement" and grounded in Nelson's baptism principle. S7 is derived "from S7a, S7b, T4, GlobalUniqueness." The causal grounding is in the prose and the dependency chain, not in the formal statement — which is exactly where it belongs. No spec change needed.

### Clean verifications (13 properties)

ArrangementFunctional, ContentImmutability, ElementLevelAddresses, FiniteArrangement, FixedDepthPositions, OriginBasedIdentity, PersistenceIndependence, ReferentialIntegrity, SpanDecomposition, StoreMonotonicity, TwoSpaceSeparation, UnrestrictedSharing, VPositionWellFormed — all verified without divergence. Type-level properties (S2 via map functionality, S8-fin via map finiteness) are correctly modeled as trivially true predicates with explanatory comments.

VERDICT: CONVERGED
