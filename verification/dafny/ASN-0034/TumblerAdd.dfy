// ASN-0034: TumblerAdd — definition (DEF)
// Tumbler addition a ⊕ w, defined component-wise:
//   k = actionPoint(w); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k.
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"

module TumblerAdd {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  // Least index j in [1, k] with a_j != 0, or 0 if none.
  // Used as the existential witness in the dominance proof of TumblerAdd.
  function FirstNonZeroInPrefix(a: Tumbler, k: nat, start: nat): nat
    requires InT(a)
    requires 1 <= start
    requires k <= Length(a)
    ensures var r := FirstNonZeroInPrefix(a, k, start);
            r == 0
            || (start <= r <= k
                && Component(a, r) != 0
                && (forall i :: start <= i < r ==> Component(a, i) == 0))
    ensures FirstNonZeroInPrefix(a, k, start) == 0
            ==> (forall i :: start <= i <= k ==> Component(a, i) == 0)
    decreases if start > k then 0 else k - start + 1
  {
    if start > k then 0
    else if Component(a, start) != 0 then start
    else FirstNonZeroInPrefix(a, k, start + 1)
  }

  function TumblerAdd(a: Tumbler, w: Tumbler): (r: Tumbler)
    requires InT(a) && InT(w)
    requires PositiveTumbler.PositiveTumbler(w)
    requires ActionPoint.ActionPoint(w) <= Length(a)
    ensures InT(r)
    ensures Length(r) == Length(w)
    ensures forall i :: 1 <= i < ActionPoint.ActionPoint(w) ==>
              Component(r, i) == Component(a, i)
    ensures Component(r, ActionPoint.ActionPoint(w)) ==
              Component(a, ActionPoint.ActionPoint(w)) +
              Component(w, ActionPoint.ActionPoint(w))
    ensures forall i :: ActionPoint.ActionPoint(w) < i <= Length(w) ==>
              Component(r, i) == Component(w, i)
    ensures LexicographicOrder.LexicographicOrder(a, r)
    ensures LexicographicOrder.LexicographicOrder(w, r) || w == r
  {
    var k := ActionPoint.ActionPoint(w);
    var result := Tumbler(a.components[..k-1]
                          + [a.components[k-1] + w.components[k-1]]
                          + w.components[k..]);
    // Seq facts derived directly from the constructor body.
    assert forall i :: 1 <= i < k ==>
      Component(result, i) == a.components[i - 1]
                           == Component(a, i);
    assert Component(result, k) == a.components[k - 1] + w.components[k - 1]
                                == Component(a, k) + Component(w, k);
    assert forall i :: k < i <= Length(w) ==>
      Component(result, i) == w.components[i - 1]
                           == Component(w, i);
    assert Length(result) == Length(w);

    var j := FirstNonZeroInPrefix(a, k, 1);
    // Case on j: 0 means all a_i = 0 for i in [1, k] (equality);
    // nonzero j gives the divergence witness for LexicographicOrder(w, result).
    if j == 0 then
      // Equality branch: each component of result equals the matching component of w.
      assert forall i :: 1 <= i <= k ==> Component(a, i) == 0;
      assert forall i :: 1 <= i < k ==> Component(result, i) == 0;
      assert forall i :: 1 <= i < k ==> Component(w, i) == 0;
      assert Component(a, k) == 0;
      assert Component(result, k) == Component(w, k);
      // Bridge to seq indexing for extensionality.
      assert forall p :: 0 <= p < |w.components| ==>
        w.components[p] == result.components[p] by {
        forall p | 0 <= p < |w.components|
          ensures w.components[p] == result.components[p]
        {
          var i := p + 1;
          assert 1 <= i <= Length(w);
          assert Component(w, i) == w.components[p];
          assert Component(result, i) == result.components[p];
          if i < k {
            assert Component(w, i) == 0;
            assert Component(result, i) == 0;
          } else if i == k {
            assert Component(result, k) == Component(w, k);
          } else {
            assert Component(result, i) == Component(w, i);
          }
        }
      };
      assert |w.components| == |result.components|;
      assert w.components == result.components;
      result
    else
      // Strict branch: j witnesses LexicographicOrder(w, result).
      assert 1 <= j <= k;
      assert Component(a, j) != 0;
      assert forall i :: 1 <= i < j ==> Component(a, i) == 0;
      assert forall i :: 1 <= i < j ==> i < k;
      assert forall i :: 1 <= i < j ==> Component(result, i) == Component(a, i) == 0;
      assert forall i :: 1 <= i < j ==> Component(w, i) == 0;
      assert forall i :: 1 <= i < j ==>
        i <= Length(w) && i <= Length(result) &&
        Component(w, i) == Component(result, i);
      assert j <= Length(w) && j <= Length(result);
      assert Less(Component(w, j), Component(result, j));
      result
  }
}
