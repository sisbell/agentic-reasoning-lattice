# Review of ASN-0043

Based on Dafny verification — 22/22 verified, no divergences reported.

## REVISE

No genuine spec issues found.

## QUALITY

### File: IdentityByAddress.dfy — SIMPLIFY

The `IdentityByAddress` predicate is a tautology:

```dafny
ghost predicate IdentityByAddress(store: Store) {
  forall a1, a2 :: a1 in store && a2 in store && a1 != a2
    ==> true  // distinct addresses are distinct entities by construction
}
```

`==> true` is vacuously true for every store. The comment acknowledges this ("by construction"), but the predicate and its proof lemma `IdentityByAddressHolds` are dead weight. L11 holds by the map representation — distinct keys are distinct entries. The only substantive content in this file is `NonInjectivityPermitted`, which serves as a useful witness that the store need not be injective.

**Suggestion:** Delete the `IdentityByAddress` predicate and `IdentityByAddressHolds` lemma. Keep `NonInjectivityPermitted` as the file's sole content — it captures the non-obvious part of L11 (that duplicate values at distinct keys are permitted).

### File: TypeByAddress.dfy — SIMPLIFY

Same pattern. `SameType` is defined as `l1.typ == l2.typ`, and then `TypeByAddress` asserts the biconditional `SameType(store[a1], store[a2]) <==> store[a1].typ == store[a2].typ` — which unfolds to `X <==> X`. The predicate is a tautology and `TypeByAddressHolds` proves it vacuously.

L8's real content — that type matching uses address comparison rather than content dereferencing — is captured by the data model itself: the type endset contains tumbler addresses, not content values. There is no content-lookup function to contrast with.

**Suggestion:** Replace the predicate/lemma pair with a comment explaining that L8 holds by construction of the `Link` datatype (type endsets store address spans, not content references). No executable predicate is needed.

### File: LinkStore.dfy — SIMPLIFY

Duplicates `Span`, `WellFormedSpan`, `Endset`, `WellFormedEndset` from Endset.dfy. Both files define identical types independently. Files downstream import one or the other, creating two incompatible type universes for the same concept:

- Coverage.dfy, SlotDistinction.dfy, DirectionalFlexibility.dfy import `Endset.dfy`
- EndsetGenerality.dfy, LinkImmutability.dfy, TypeGhostPermission.dfy import `LinkStore.dfy`

**Suggestion:** LinkStore.dfy should import Endset.dfy and Link.dfy, re-exporting their types rather than redefining them. The `Store` type and `WellFormedStore` predicate are LinkStore.dfy's actual contribution.

### File: ReflexiveAddressing.dfy + TypeHierarchyByContainment.dfy — SIMPLIFY

`UnitDisplacement` and `UnitDisplacementPositive` are duplicated verbatim between these two files:

```dafny
// In both files:
function UnitDisplacement(n: nat): Tumbler
  requires n >= 1
{ Tumbler(Zeros(n - 1) + [1]) }

lemma UnitDisplacementPositive(n: nat)
  requires n >= 1
  ensures PositiveTumbler(UnitDisplacement(n))
  ensures ActionPoint(UnitDisplacement(n)) == n - 1
{ assert UnitDisplacement(n).components[n - 1] == 1; }
```

**Suggestion:** Factor into a shared module (e.g., `SpanConstruction.dfy` or add to the existing tumbler algebra). Both files import and use.

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
### File: LinkStoreMonotonicity.dfy — PASS
### File: OwnershipEndsetIndependence.dfy — PASS
### File: SlotDistinction.dfy — PASS
### File: SubspacePartition.dfy — PASS
### File: TripleEndsetStructure.dfy — PASS
### File: TypeGhostPermission.dfy — PASS

## SKIP

### All 22 properties verified without divergence

No preconditions were added, no conclusions weakened, no invariants strengthened beyond what the ASN states. The Dafny encoding faithfully models the ASN properties. Proof artifacts (empty lemma bodies, `assert` hints for solver guidance in TypeGhostPermission and ReflexiveAddressing) are appropriate mechanical concerns that do not reflect on the spec.

VERDICT: SIMPLIFY
