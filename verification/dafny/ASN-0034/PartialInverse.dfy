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

    if Component(a, k) == 0 {
      // Case A: a is the zero tumbler.  Show r == w, then TumblerSub(w, w)
      // is the zero tumbler of length k, which is a.
      forall i | 1 <= i <= k
        ensures Component(r, i) == Component(w, i)
      { }
      Extensionality(r, w);

      var s := TumblerSub.TumblerSub(w, w);
      forall i | 1 <= i <= k
        ensures Component(s, i) == Component(a, i)
      { }
      Extensionality(s, a);
    } else {
      // Case B: a[k] != 0, so r[k] > w[k] and zpd(r, w) = k.
      assert forall i :: 1 <= i < k ==>
        PaddedComponent(r, i) == PaddedComponent(w, i);
      FirstPaddedMismatchAdvance(r, w, 1, k, k);

      var s := TumblerSub.TumblerSub(r, w);
      forall i | 1 <= i <= k
        ensures Component(s, i) == Component(a, i)
      { }
      Extensionality(s, a);
    }
  }
}
