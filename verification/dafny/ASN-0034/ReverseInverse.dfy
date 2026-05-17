// ASN-0034: ReverseInverse — (a ⊖ w) ⊕ w = a
// Tumbler subtraction and addition are mutually inverse when a ≥ w, Pos(w),
// k = #a = #w, action point of w is k, and a's components before k are zero.
include "./TumblerAdd.dfy"
include "./TumblerSub.dfy"
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./ZeroPaddedDivergence.dfy"
include "./NatStrictTotalOrder.dfy"

module ReverseInverse {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened TumblerAdd
  import opened TumblerSub
  import opened ZeroPaddedDivergence
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  lemma ReverseInverse(a: Tumbler, w: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires LexicographicOrder.LexicographicOrder(w, a) || w == a
    requires Length(a) == Length(w)
    requires ActionPoint.ActionPoint(w) == Length(w)
    requires forall i :: 1 <= i < Length(a) ==> Component(a, i) == 0
    ensures TumblerAdd.TumblerAdd(TumblerSub.TumblerSub(a, w), w) == a
  {
    var k := Length(w);
    var r := TumblerSub.TumblerSub(a, w);

    if a == w {
      // Case A: r is the zero tumbler.
      var s := TumblerAdd.TumblerAdd(r, w);
      forall i | 1 <= i <= k
        ensures Component(s, i) == Component(a, i)
      { }
      Extensionality(s, a);
    } else {
      // Case B: a != w. Components agree on 1..k-1 (both zero), differ at k.
      assert forall i :: 1 <= i < k ==>
        PaddedComponent(a, i) == PaddedComponent(w, i);
      assert PaddedComponent(a, k) != PaddedComponent(w, k) by {
        if PaddedComponent(a, k) == PaddedComponent(w, k) {
          forall i | 1 <= i <= k
            ensures Component(a, i) == Component(w, i)
          { }
          Extensionality(a, w);
        }
      }
      FirstPaddedMismatchAdvance(a, w, 1, k, k);

      var s := TumblerAdd.TumblerAdd(r, w);
      forall i | 1 <= i <= k
        ensures Component(s, i) == Component(a, i)
      { }
      Extensionality(s, a);
    }
  }
}
