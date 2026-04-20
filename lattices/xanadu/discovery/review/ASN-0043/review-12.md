# Review of ASN-0043

Based on Dafny verification — 24 properties, 3 divergences, 21 clean

## REVISE

No genuine spec issues identified. All divergences are proof artifacts.

## QUALITY

### File: Coverage.dfy — PASS
### File: DirectionalFlexibility.dfy — PASS
### File: DualPrimitive.dfy — PASS
### File: Endset.dfy — PASS
### File: EndsetGenerality.dfy — PASS
### File: EndsetSetSemantics.dfy — PASS
### File: Home.dfy — PASS
### File: Link.dfy — PASS
### File: LinkElementLevel.dfy — PASS
### File: LinkImmutability.dfy — PASS
### File: LinkScopedAllocation.dfy — PASS

### File: LinkStore.dfy — SIMPLIFY

**Missing abstraction / type duplication.** LinkStore.dfy defines its own `Span`, `WellFormedSpan`, `Endset`, `WellFormedEndset`, `Link`, `WellFormedLink` — all of which already exist in Endset.dfy and Link.dfy. Half the modules import from LinkStore, the other half from Endset/LinkDef, creating parallel type hierarchies that happen to be structurally identical but are distinct Dafny types.

LinkStore.dfy should import and re-export from Endset.dfy and Link.dfy, defining only the `Store` type and `WellFormedStore` predicate. All downstream modules should use a single type hierarchy.

### File: LinkStoreMonotonicity.dfy — SIMPLIFY

**Type duplication (worse).** Defines its own complete type stack — `Span`, `Endset`, `Link`, `LinkStore`, and `LinkImmutability` — all inline, disconnected from every other module. This is the third independent definition of the core types.

Should import from LinkStore.dfy (once that imports from Endset/Link) and from LinkImmutability.dfy. The file should contain only the monotonicity lemma:

```dafny
include "LinkImmutability.dfy"
include "LinkStore.dfy"

module LinkStoreMonotonicity {
  import opened LinkStore
  import LinkImmutability

  lemma LinkStoreMonotonicity(before: Store, after: Store)
    requires LinkImmutability.LinkImmutability(before, after)
    ensures before.Keys <= after.Keys
  { }
}
```

### File: LinkUniqueness.dfy — PASS
### File: NonInjectivity.dfy — PASS
### File: OwnershipEndsetIndependence.dfy — PASS
### File: PrefixSpanCoverage.dfy — PASS
### File: ReflexiveAddressing.dfy — PASS
### File: SlotDistinction.dfy — PASS
### File: SubspacePartition.dfy — PASS
### File: TripleEndsetStructure.dfy — PASS
### File: TypeByAddress.dfy — PASS
### File: TypeGhostPermission.dfy — PASS
### File: TypeHierarchyByContainment.dfy — PASS

## SKIP

### Artifact 1: Incomplete state-machine modeling (LinkUniqueness, NonInjectivity, TypeGhostPermission)

All three divergences share the same shape: the ASN proves properties over conforming states satisfying the full L0–L14 invariant suite, while the Dafny models capture the structural core without modeling the complete state machine or T9 forward allocation.

- **LinkUniqueness** — ASN derives from T9 + GlobalUniqueness as a system-level allocation property. Dafny encodes GlobalUniqueness's structural discriminants (ordering, non-prefix, or different length) as a precondition. The T9 protocol is operational, not structural — the ASN doesn't need to change.

- **NonInjectivity** — ASN proves the extended state Sigma' preserves L0–L14. Dafny proves the structural core: fresh addresses exist (by unboundedness) and can carry the same link value. Full invariant preservation would require encoding L0–L14 as a state predicate and checking each conjunct — an encoding concern, not a spec gap.

- **TypeGhostPermission** — Same pattern. ASN proves full conformance of the witness state. Dafny proves the witness construction is well-formed (span satisfies T12, ghost address is outside entity stores). The precondition `a != g` is noted as following from L0/T7 (subspace separation), which is correct.

These are all artifacts of the Dafny model's scope boundary. The ASN properties are stated correctly; the proofs verify the structural core that makes each property hold. No spec revision needed.

VERDICT: SIMPLIFY
