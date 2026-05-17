// ASN-0034: TA5 — HierarchicalIncrement (DEF)
// inc(t, k): when k = 0, modify position sig(t) to t_{sig(t)} + 1;
// when k > 0, extend by k positions with k - 1 zeros and final 1.
include "./CarrierSetDefinition.dfy"
include "./LastSignificantPosition.dfy"
include "./LexicographicOrder.dfy"

module HierarchicalIncrement {
  import opened CarrierSetDefinition
  import opened LastSignificantPosition
  import opened LexicographicOrder
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  function HierarchicalIncrement(t: Tumbler, k: nat): (t': Tumbler)
    requires InT(t)
    ensures InT(t')
    // (c) k == 0: length preserved, modification only at sig(t)
    ensures k == 0 ==> Length(t') == Length(t)
    ensures k == 0 ==>
      Component(t', LastSignificantPosition.LastSignificantPosition(t)) ==
      Component(t, LastSignificantPosition.LastSignificantPosition(t)) + 1
    ensures k == 0 ==>
      forall i :: 1 <= i <= Length(t) &&
                  i != LastSignificantPosition.LastSignificantPosition(t) ==>
        Component(t', i) == Component(t, i)
    // (d) k > 0: length = #t + k, with k - 1 zeros and final 1
    ensures k > 0 ==> Length(t') == Length(t) + k
    ensures k > 0 ==>
      forall i :: 1 <= i <= Length(t) ==> Component(t', i) == Component(t, i)
    ensures k > 0 ==>
      forall i :: Length(t) + 1 <= i < Length(t) + k ==>
        Component(t', i) == 0
    ensures k > 0 ==> Component(t', Length(t) + k) == 1
    // (a) strict increase under T1
    ensures LexicographicOrder.LexicographicOrder(t, t')
  {
    if k == 0 then
      var p := LastSignificantPosition.LastSignificantPosition(t);
      Tumbler(t.components[..p-1] + [t.components[p-1] + 1] + t.components[p..])
    else
      Tumbler(t.components + seq(k - 1, _ => 0 as Carrier) + [1 as Carrier])
  }
}
