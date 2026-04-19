include "./TumblerAdd.dfy"
include "./CanonicalRepresentation.dfy"

module LeftCancellation {
  // TA-LC — LeftCancellation
  // If a ⊕ x = a ⊕ y with both sides well-defined, then x = y.

  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import TA = TumblerAdd
  import CanonicalRepresentation

  lemma ActionPointsEqual(a: Tumbler, x: Tumbler, y: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(x) && IsPositive(x)
    requires ValidTumbler(y) && IsPositive(y)
    requires TA.ActionPoint(x) < |a.components|
    requires TA.ActionPoint(y) < |a.components|
    requires TA.TumblerAdd(a, x) == TA.TumblerAdd(a, y)
    ensures TA.ActionPoint(x) == TA.ActionPoint(y)
  {
    var kx := TA.ActionPoint(x);
    var ky := TA.ActionPoint(y);
    var rx := TA.TumblerAdd(a, x);
    var ry := TA.TumblerAdd(a, y);
    if kx < ky {
      assert rx.components[kx] == a.components[kx] + x.components[kx];
      assert ry.components[kx] == a.components[kx];
    } else if ky < kx {
      assert ry.components[ky] == a.components[ky] + y.components[ky];
      assert rx.components[ky] == a.components[ky];
    }
  }

  // TumblerAdd result has the displacement's tail components after k
  lemma TailComponents(a: Tumbler, w: Tumbler, i: nat)
    requires ValidTumbler(a) && ValidTumbler(w) && IsPositive(w)
    requires TA.ActionPoint(w) < |a.components|
    requires var k := TA.ActionPoint(w); k < i < |w.components|
    ensures TA.TumblerAdd(a, w).components[i] == w.components[i]
  {
    var k := TA.ActionPoint(w);
    var r := a.components[..k] + [a.components[k] + w.components[k]] + w.components[k+1..];
    assert r[i] == w.components[k+1..][i - k - 1] == w.components[i];
  }

  lemma LeftCancellation(a: Tumbler, x: Tumbler, y: Tumbler)
    requires ValidTumbler(a)
    requires ValidTumbler(x) && IsPositive(x)
    requires ValidTumbler(y) && IsPositive(y)
    requires TA.ActionPoint(x) < |a.components|
    requires TA.ActionPoint(y) < |a.components|
    requires TA.TumblerAdd(a, x) == TA.TumblerAdd(a, y)
    ensures x == y
  {
    ActionPointsEqual(a, x, y);
    var k := TA.ActionPoint(x);
    var rx := TA.TumblerAdd(a, x);
    var ry := TA.TumblerAdd(a, y);
    assert |x.components| == |y.components|;
    assert rx.components[k] == a.components[k] + x.components[k];
    assert ry.components[k] == a.components[k] + y.components[k];
    forall i | k < i < |x.components|
      ensures x.components[i] == y.components[i]
    {
      TailComponents(a, x, i);
      TailComponents(a, y, i);
    }
    assert forall i :: 0 <= i < k ==> x.components[i] == 0 && y.components[i] == 0;
  }
}
