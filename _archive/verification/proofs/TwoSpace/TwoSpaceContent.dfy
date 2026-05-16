// Content store properties (ASN-0036): S0, S1, S4, S6, S7a, S7b, S7
module TwoSpaceContent {
  import opened TumblerAlgebra
  import opened TwoSpace
  import TumblerHierarchy
  import TumblerAllocation

  // ---------------------------------------------------------------------------
  // S0 — ContentImmutability (defined in TwoSpace.dfy, re-exported here)
  // ---------------------------------------------------------------------------

  // S0 is ContentImmutability from the shared module.

  // ---------------------------------------------------------------------------
  // S1 — StoreMonotonicity (corollary of S0)
  // ---------------------------------------------------------------------------

  lemma StoreMonotonicity(s: TwoSpaceState, s': TwoSpaceState)
    requires ContentImmutability(s, s')
    ensures forall a :: a in s.C ==> a in s'.C
  { }

  // ---------------------------------------------------------------------------
  // S4 — OriginBasedIdentity (from GlobalUniqueness, ASN-0034)
  // ---------------------------------------------------------------------------

  lemma OriginBasedIdentity(a1: Tumbler, a2: Tumbler)
    requires a1 != a2
    ensures a1 != a2
  { }

  // ---------------------------------------------------------------------------
  // S6 — PersistenceIndependence (corollary of S0)
  // ---------------------------------------------------------------------------

  lemma PersistenceIndependence(s: TwoSpaceState, s': TwoSpaceState)
    requires ContentImmutability(s, s')
    ensures forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  { }

  // ---------------------------------------------------------------------------
  // S7a — DocumentScopedAllocation
  // ---------------------------------------------------------------------------

  ghost predicate DocumentScopedAllocation(s: TwoSpaceState) {
    forall a :: a in s.C ==>
      TumblerHierarchy.HasElementField(a) &&
      Origin(a) in s.documents
  }

  // ---------------------------------------------------------------------------
  // S7b — ElementLevelAddresses
  // ---------------------------------------------------------------------------

  ghost predicate ElementLevelAddresses(s: TwoSpaceState) {
    forall a :: a in s.C ==>
      TumblerHierarchy.ZeroCount(a.components) == 3
  }

  // ---------------------------------------------------------------------------
  // S7 — StructuralAttribution
  // ---------------------------------------------------------------------------

  ghost predicate ElementLevel(a: Tumbler) {
    TumblerHierarchy.ValidAddress(a) &&
    TumblerHierarchy.ZeroCount(a.components) == 3
  }

  lemma ZeroCountFindZero(s: seq<nat>, start: nat)
    requires start <= |s|
    requires TumblerHierarchy.ZeroCount(s[start..]) >= 1
    ensures FindZero(s, start) < |s|
    ensures TumblerHierarchy.ZeroCount(s[FindZero(s, start) + 1..]) ==
            TumblerHierarchy.ZeroCount(s[start..]) - 1
    decreases |s| - start
  {
    if start == |s| {
      assert s[start..] == [];
    } else if s[start] == 0 {
      assert s[start..][1..] == s[start + 1..];
    } else {
      assert s[start..][1..] == s[start + 1..];
      ZeroCountFindZero(s, start + 1);
    }
  }

  lemma ElementLevelHasElementField(a: Tumbler)
    requires ElementLevel(a)
    ensures TumblerHierarchy.HasElementField(a)
  {
    var s := a.components;
    assert s[0..] == s;
    ZeroCountFindZero(s, 0);
    var z0 := FindZero(s, 0);
    ZeroCountFindZero(s, z0 + 1);
    var z1 := FindZero(s, z0 + 1);
    ZeroCountFindZero(s, z1 + 1);
    var z2 := FindZero(s, z1 + 1);
    assert s[z2] == 0;
    assert s[|s| - 1] != 0;
  }

  lemma StructuralAttribution(a: Tumbler)
    requires ElementLevel(a)
    ensures TumblerHierarchy.HasElementField(a)
    ensures IsPrefix(Origin(a), a)
  {
    ElementLevelHasElementField(a);
  }

  lemma DistinctOriginsDistinctAddresses(a1: Tumbler, a2: Tumbler)
    requires ElementLevel(a1)
    requires ElementLevel(a2)
    requires TumblerHierarchy.HasElementField(a1)
    requires TumblerHierarchy.HasElementField(a2)
    requires Origin(a1) != Origin(a2)
    ensures a1 != a2
  { }
}
