// ASN-0034: TA4 — PartialInverse
// (a ⊕ w) ⊖ w = a holds exactly when ActionPoint(w) = #a = #w and the
// components of a strictly before that position are zero.
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./NatStrictTotalOrder.dfy"

module PartialInverse {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened ZeroPaddedDivergence
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  lemma PartialInverse(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires Length(a) == Length(w)
    requires ActionPoint.ActionPoint(w) == Length(w)
    requires forall i :: 1 <= i < Length(a) ==> Component(a, i) == 0
    ensures TumblerSub.TumblerSub(TumblerAdd.TumblerAdd(a, w), w) == a
  {
    var k := Length(w);
    var r := TumblerAdd.TumblerAdd(a, w);
    assert Length(r) == k;
    assert forall i :: 1 <= i < k ==> Component(r, i) == Component(a, i);
    assert Component(r, k) == Component(a, k) + Component(w, k);

    if Component(a, k) == 0 {
      // Case A: a is the zero tumbler.  Show r == w, then TumblerSub(w, w) is
      // the zero tumbler of length k, which is a.
      forall i | 1 <= i <= k
        ensures Component(r, i) == Component(w, i)
      {
        if i < k {
          assert Component(a, i) == 0;
        } else {
          assert i == k;
          assert Component(r, k) == 0 + Component(w, k);
        }
      }
      Extensionality(r, w);
      assert r == w;

      var s := TumblerSub.TumblerSub(w, w);
      assert ZeroPaddedDivergence.ZeroPaddedDivergence(w, w) == 0;
      assert ZeroTumbler(s);
      assert Length(s) == k;

      forall i | 1 <= i <= k
        ensures Component(s, i) == Component(a, i)
      { }
      Extensionality(s, a);
    } else {
      // Case B: a[k] != 0, so r[k] > w[k] and zpd(r, w) = k.
      assert Component(a, k) != 0;
      assert Component(r, k) > Component(w, k);

      // For i < k, both r[i] and w[i] are zero.
      assert forall i :: 1 <= i < k ==> Component(r, i) == 0;
      assert forall i :: 1 <= i < k ==> Component(w, i) == 0;

      // Compute zpd(r, w) = k.
      assert ZeroPaddedDivergence.ZeroPaddedDivergence(r, w) == k;

      var s := TumblerSub.TumblerSub(r, w);
      assert Length(s) == k;
      assert ActionPoint.ActionPoint(s) == k;
      assert PositiveTumbler.PositiveTumbler(s);

      // For i < k, ActionPoint(s) = k means Component(s, i) == 0.
      assert forall i :: 1 <= i < k ==> Component(s, i) == 0;

      // Component(s, k) = SatSub(r[k], w[k]) = a[k].
      assert Component(s, k) == Component(a, k);

      forall i | 1 <= i <= k
        ensures Component(s, i) == Component(a, i)
      { }
      Extensionality(s, a);
    }
  }
}
