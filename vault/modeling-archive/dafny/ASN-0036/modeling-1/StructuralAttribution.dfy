include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// S7 — StructuralAttribution
module StructuralAttribution {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // S7b — Element-level addresses have exactly 3 zero separators
  ghost predicate ElementLevel(a: Tumbler) {
    TumblerHierarchy.ValidAddress(a) &&
    TumblerHierarchy.ZeroCount(a.components) == 3
  }

  // Origin as field decomposition — N.0.U.0.D
  function OriginFields(a: Tumbler): seq<nat> {
    TumblerHierarchy.NodeField(a) + [0] +
    TumblerHierarchy.UserField(a) + [0] +
    TumblerHierarchy.DocField(a)
  }

  // If ZeroCount from position start >= 1, FindZero finds a zero within bounds
  // and the remaining ZeroCount decreases by 1.
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

  // Element-level addresses have an element field (all four fields present)
  lemma ElementLevelHasElementField(a: Tumbler)
    requires ElementLevel(a)
    ensures TumblerHierarchy.HasElementField(a)
  {
    var s := a.components;
    assert s[0..] == s;

    // First zero
    ZeroCountFindZero(s, 0);
    var z0 := FindZero(s, 0);
    // z0 < |s|, ZeroCount(s[z0+1..]) == 2

    // Second zero
    ZeroCountFindZero(s, z0 + 1);
    var z1 := FindZero(s, z0 + 1);
    // z1 < |s|, ZeroCount(s[z1+1..]) == 1

    // Third zero
    ZeroCountFindZero(s, z1 + 1);
    var z2 := FindZero(s, z1 + 1);
    // z2 < |s|, ZeroCount(s[z2+1..]) == 0

    // Last component is nonzero (ValidAddress), z2 is a zero, so z2 < |s| - 1
    // Therefore E1Pos(a) = z2 + 1 < |s| = HasElementField
    assert s[z2] == 0;
    assert s[|s| - 1] != 0;
  }

  // S7 — StructuralAttribution
  // For element-level addresses, the document-level origin (N.0.U.0.D)
  // is a structural prefix of the address. Document attribution is embedded
  // in the address — it cannot be stripped or forged.
  // Derived from S7a, S7b, T4 (ASN-0034).
  //
  // DIVERGENCE: The ASN states that origin "uniquely identifies the allocating
  // document." This provenance guarantee depends on the allocation protocol
  // (S7a, T9/T10 from ASN-0034) — a system-level invariant that cannot be
  // expressed as a structural precondition. The lemma captures the structural
  // core: origin is well-defined, equals the field decomposition, and is a
  // prefix of the address.
  lemma StructuralAttribution(a: Tumbler)
    requires ElementLevel(a)
    ensures TumblerHierarchy.HasElementField(a)
    ensures IsPrefix(Tumbler(OriginFields(a)), a)
  {
    ElementLevelHasElementField(a);
  }

  // Corollary: addresses with distinct origins are distinct
  lemma DistinctOriginsDistinctAddresses(a1: Tumbler, a2: Tumbler)
    requires ElementLevel(a1)
    requires ElementLevel(a2)
    requires OriginFields(a1) != OriginFields(a2)
    ensures a1 != a2
  { }
}
