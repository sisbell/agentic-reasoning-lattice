# Verification Status — modeling-1

Updated: 2026-03-16 15:25
Verified: 22/22

| Property | Status | Divergences |
|----------|--------|-------------|
| StructuralOwnership | verified |  |
| PrefixDetermination | verified |  |
| AccountBoundary | verified |  |
| PrefixInjective | verified | With Principal modeled as a datatype whose sole field is the prefix tumbler, inj... |
| OwnershipExclusivity | verified |  |
| OwnershipRefinement | verified | Prefix immutability is structural in this model. Since Principal embeds its pref... |
| DomainCoverage | verified |  |
| SubdivisionAuthority | verified | allocated_by is modeled as an explicit allocator map (Tumbler → Principal) rathe... |
| StructuralProvenance | verified | The ASN states O6 over ω (effective owner) and Σ.alloc. The Dafny model captures... |
| OwnershipDelegation | verified |  |
| IrrevocableDelegation | verified |  |
| NodeLocalOwnership | verified |  |
| DenialAsFork | verified |  |
| IdentityAxiomatic | verified | O11 is a meta-property — it asserts that identity binding is assumed (axiomatic)... |
| PrincipalPersistence | verified |  |
| PrefixImmutable | verified |  |
| BootstrapPrincipal | verified |  |
| PrincipalClosure | verified |  |
| AllocationClosure | verified | allocated_by is modeled as an allocator map (Tumbler → Principal) consistent wit... |
| AllocatedAddressValid | verified |  |
| AccountPrefix | verified |  |
| AccountPermanence | verified | The ASN states AccountPermanence as a trace-level inductive property over reacha... |
