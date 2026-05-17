// ASN-0034: TA-LC — LeftCancellation
// (A a, x, y ∈ T : Pos(x) ∧ Pos(y) ∧ actionPoint(x) ≤ #a ∧ actionPoint(y) ≤ #a :
//    a ⊕ x = a ⊕ y ⇒ x = y).
include "./TumblerAdd.dfy"
include "./WellDefinedAddition.dfy"
include "./NatAdditionCancellation.dfy"

module LeftCancellation {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened TumblerAdd
  import opened NatAdditionCancellation
  import opened NatCarrierSet

  // If a ⊕ x = a ⊕ y, the action points must agree. Otherwise the result at
  // the smaller action point would differ: side with the smaller k injects a
  // nonzero summand there; the other side leaves a[k] untouched.
  lemma ActionPointsEqual(a: Tumbler, x: Tumbler, y: Tumbler)
    requires InT(a) && InT(x) && InT(y)
    requires PositiveTumbler.PositiveTumbler(x)
    requires PositiveTumbler.PositiveTumbler(y)
    requires ActionPoint.ActionPoint(x) <= Length(a)
    requires ActionPoint.ActionPoint(y) <= Length(a)
    requires TumblerAdd.TumblerAdd(a, x) == TumblerAdd.TumblerAdd(a, y)
    ensures ActionPoint.ActionPoint(x) == ActionPoint.ActionPoint(y)
  {
    var kx := ActionPoint.ActionPoint(x);
    var ky := ActionPoint.ActionPoint(y);
    var rx := TumblerAdd.TumblerAdd(a, x);
    var ry := TumblerAdd.TumblerAdd(a, y);
    if kx < ky {
      assert Component(rx, kx) == Component(a, kx) + Component(x, kx);
      assert Component(ry, kx) == Component(a, kx);
      assert Component(x, kx) != 0;
      NatAdditionSummandAbsorption(Component(a, kx), Component(x, kx));
    } else if ky < kx {
      assert Component(ry, ky) == Component(a, ky) + Component(y, ky);
      assert Component(rx, ky) == Component(a, ky);
      assert Component(y, ky) != 0;
      NatAdditionSummandAbsorption(Component(a, ky), Component(y, ky));
    }
  }

  lemma LeftCancellation(a: Tumbler, x: Tumbler, y: Tumbler)
    requires InT(a) && InT(x) && InT(y)
    requires PositiveTumbler.PositiveTumbler(x)
    requires PositiveTumbler.PositiveTumbler(y)
    requires ActionPoint.ActionPoint(x) <= Length(a)
    requires ActionPoint.ActionPoint(y) <= Length(a)
    requires TumblerAdd.TumblerAdd(a, x) == TumblerAdd.TumblerAdd(a, y)
    ensures x == y
  {
    ActionPointsEqual(a, x, y);
    var k := ActionPoint.ActionPoint(x);
    var rx := TumblerAdd.TumblerAdd(a, x);
    var ry := TumblerAdd.TumblerAdd(a, y);
    assert Length(x) == Length(y);
    forall i | 1 <= i <= Length(x)
      ensures Component(x, i) == Component(y, i)
    {
      if i < k {
      } else if i == k {
        NatAdditionLeftCancellation(Component(a, k), Component(x, k), Component(y, k));
      } else {
      }
    }
    Extensionality(x, y);
  }
}
