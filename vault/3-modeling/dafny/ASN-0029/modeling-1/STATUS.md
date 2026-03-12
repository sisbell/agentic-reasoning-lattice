# Verification Status — modeling-1

Updated: 2026-03-12 01:05
Verified: 26/26

| Property | Status | Divergences |
|----------|--------|-------------|
| ValidAccountAddr | verified |  |
| AccountPrefix | verified |  |
| EmptyCreation | verified | Foundation.State lacks Σ.pub (publication status). DocState extends Foundation's... |
| DocumentAllocation | verified | allocated_before(d1, d2) is encoded by parameter ordering convention, not as an ... |
| DocumentPermanence | verified |  |
| StructuralOwnership | verified |  |
| OwnershipPermanence | verified |  |
| OwnershipRights | verified | Foundation.State lacks publication status and associate lists introduced by ASN-... |
| IdentityByAddress | verified |  |
| OriginTraceability | verified |  |
| DocumentScopedAllocation | verified |  |
| HomeDocumentMembership | verified | The ASN derives D7b from D7a, P2, and D2 as separate transition-level properties... |
| InclusionNonDestruction | verified |  |
| EditIsolation | verified |  |
| PublicationStatus | verified |  |
| PublicationMonotonicity | verified |  |
| PublicationFrame | verified |  |
| PublishOperation | verified | account(d) = actor(op) precondition omitted. Authorization is a protocol-layer c... |
| PublicationSurrender | verified | Part (d) is a transition invariant already captured by D10 (PublicationMonotonic... |
| VersionCreation | verified |  |
| VersionPlacement | verified |  |
| VersionForest | verified |  |
| DocFieldWellFormed | verified |  |
| OwnerExclusiveModification | verified | predicate(State, DocId) cannot bind the actor (external to the state). Added act... |
| NonOwnerForking | verified | predicate(State, DocId) cannot express the transition response (fork creation in... |
| ContentBasedDiscovery | verified |  |
