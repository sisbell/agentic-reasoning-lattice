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

    // Dominance proof — case split on whether any aᵢ > 0 for i ∈ [1, k]
    assert LexicographicOrder.LexicographicOrder(w, result) || w == result by {
      if exists i :: 1 <= i <= k && Component(a, i) != 0 {
        // Strict branch: pick the least such j (Hilbert choice; existence supplied
        // by the exists-witness, with the forall asserting minimality).
        var j :| 1 <= j <= k
              && Component(a, j) != 0
              && (forall i :: 1 <= i < j ==> Component(a, i) == 0);
        // At positions i < j: w_i = 0 (ActionPoint, since j ≤ k), a_i = 0 (minimality),
        // result_i: if i < k then a_i = 0 = w_i; impossible i ≥ k here since j ≤ k.
        // At position j: w_j = 0 if j < k (ActionPoint); result_j = a_j if j < k.
        // If j = k: w_k ≥ 1, result_k = a_k + w_k > w_k (since a_k > 0).
        assert forall i :: 1 <= i < j ==> i <= Length(w) && i <= Length(result) &&
                            Component(w, i) == Component(result, i);
        if j < k {
          assert Component(w, j) == 0;
          assert Component(result, j) == Component(a, j);
          assert Component(a, j) != 0;
          assert Component(w, j) < Component(result, j);
        } else {
          assert j == k;
          assert Component(result, k) == Component(a, k) + Component(w, k);
          assert Component(a, k) != 0;
          assert Component(w, k) < Component(result, k);
        }
        assert j <= Length(w) && j <= Length(result) &&
               Less(Component(w, j), Component(result, j));
      } else {
        // Equality branch: all a_i = 0 for i ∈ [1, k]
        // Therefore for each position p, result.components[p] equals w.components[p]
        assert forall i :: 1 <= i <= k ==> Component(a, i) == 0;
        // For i < k: result_i = a_i = 0 = w_i
        // For i = k: result_k = a_k + w_k = 0 + w_k = w_k
        // For i > k: result_i = w_i
        assert Length(w) == Length(result);
        assert forall i :: 1 <= i <= Length(w) ==>
                 Component(w, i) == Component(result, i);
        // Reduce Tumbler equality to seq equality
        assert w.components == result.components;
      }
    };
    result
  }
}
