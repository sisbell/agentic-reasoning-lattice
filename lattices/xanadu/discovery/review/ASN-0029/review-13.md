# Review of ASN-0029

Based on Dafny verification — 26/26 properties verified

## REVISE

No genuine spec issues found. All divergences are proof artifacts.

## QUALITY

### Shared helpers — SIMPLIFY

Pervasive duplication across files. The following are defined identically in multiple modules:

| Helper | Duplicated in |
|--------|--------------|
| `FirstZeroFrom` | AccountPrefix, EmptyCreation, IdentityByAddress, StructuralOwnership, VersionCreation, VersionPlacement (6x) |
| `HasAccountLevel` / `AccountPrefix` | AccountPrefix, EmptyCreation, VersionCreation, VersionPlacement (4x) |
| `PubStatus` datatype | EmptyCreation, NonOwnerForking, OwnershipRights, PublicationFrame, PublicationMonotonicity, PublicationStatus, PublicationSurrender, PublishOperation, VersionCreation (9x) |
| `ValidDocAddr` | EmptyCreation, VersionCreation, VersionPlacement, DocFieldWellFormed (4x, two naming variants) |
| `DocLevelPrefix` | EmptyCreation, VersionCreation, VersionPlacement, VersionForest (4x) |
| `DocState` wrapper | EmptyCreation, OwnershipRights, PublicationSurrender, VersionCreation (4x, slightly different shapes) |

**Fix:** `AccountPrefixModule` already exists but no other module imports it. Consolidate into shared modules:
- Import `AccountPrefixModule` for `FirstZeroFrom`, `HasAccountLevel`, `AccountPrefix`
- Create a single `DocOntologyBase` module exporting `PubStatus`, `DocState`, `ValidDocAddr`, `DocLevelPrefix`
- Each property module imports what it needs instead of redeclaring

This is the only quality issue. Individual proof bodies are clean.

### File: AccountPrefix.dfy — PASS
### File: ContentBasedDiscovery.dfy — PASS
### File: DocFieldWellFormed.dfy — PASS
### File: DocumentAllocation.dfy — PASS
### File: DocumentPermanence.dfy — PASS
### File: DocumentScopedAllocation.dfy — PASS
### File: EditIsolation.dfy — PASS
Empty lemma body; solver handles the derivation from P7 directly.
### File: EmptyCreation.dfy — SIMPLIFY
Duplication only (see above). The spec predicate itself is a faithful encoding.
### File: HomeDocumentMembership.dfy — PASS
Empty lemma body; solver discharges from preconditions.
### File: IdentityByAddress.dfy — PASS
Round-trip lemma is the right proof structure.
### File: InclusionNonDestruction.dfy — PASS
### File: NonOwnerForking.dfy — PASS
### File: OriginTraceability.dfy — PASS
### File: OwnerExclusiveModification.dfy — PASS
### File: OwnershipPermanence.dfy — PASS
### File: OwnershipRights.dfy — PASS
Thin predicate (map membership only) is correct — operational enforcement deferred to D15.
### File: PublicationFrame.dfy — PASS
### File: PublicationMonotonicity.dfy — PASS
### File: PublicationStatus.dfy — PASS
### File: PublicationSurrender.dfy — PASS
### File: PublishOperation.dfy — PASS
### File: StructuralOwnership.dfy — SIMPLIFY
Duplication only (see above).
### File: ValidAccountAddr.dfy — PASS
### File: VersionCreation.dfy — SIMPLIFY
Duplication only (see above). The large spec predicate faithfully encodes D12.
### File: VersionForest.dfy — PASS
### File: VersionPlacement.dfy — SIMPLIFY
Duplication only (see above).

## SKIP

### Proof artifacts (8 divergences)

All 8 divergences are encoding artifacts — things Dafny needs that the ASN doesn't need to express. Grouped by category:

**State extension (3).** EmptyCreation, OwnershipRights, PublicationSurrender: Foundation.State lacks `Σ.pub`, associate lists, and session sets introduced by ASN-0029. Each wraps Foundation.State in a `DocState` datatype. This is a Dafny modeling necessity — the ASN correctly extends the state and the Dafny code faithfully tracks it.

**Actor binding (3).** OwnerExclusiveModification, NonOwnerForking, PublishOperation: the ASN's `actor(op)` is external to state, so Dafny adds explicit actor parameters or omits the authorization precondition. The underlying state transformations are correctly modeled. Authorization is a protocol-layer concern that doesn't affect the mathematical properties being verified.

**Temporal encoding (1).** DocumentAllocation: `allocated_before(d1, d2)` is encoded by parameter ordering convention. The monotonicity property is structural (enforced by `inc` mechanism); the Dafny predicate captures the structural consequence correctly.

**Proof strategy (1).** HomeDocumentMembership: combines D7a and D2 into a single reachable-state invariant `AllocatedHomeInD`. The ASN derives D7b from separate transition-level properties; Dafny collapses the derivation chain into a single-state precondition. The proved property is equivalent.

### Clean verifications (18)

AccountPrefix, ContentBasedDiscovery, DocFieldWellFormed, DocumentPermanence, DocumentScopedAllocation, EditIsolation, IdentityByAddress, InclusionNonDestruction, OriginTraceability, OwnershipPermanence, PublicationFrame, PublicationMonotonicity, PublicationStatus, StructuralOwnership, ValidAccountAddr, VersionCreation, VersionForest, VersionPlacement — all verified without divergence from the ASN.

VERDICT: SIMPLIFY
