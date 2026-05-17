// ASN-0034: TA-PosDom — PositiveDominatesZero
// (A t ∈ T, z ∈ T : Pos(t) ∧ Zero(z) :: z < t)
// Every positive tumbler dominates every zero tumbler under T1.
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./PositiveTumbler.dfy"
include "./NatStrictTotalOrder.dfy"
include "./NatZeroMinimum.dfy"

module PositiveDominatesZero {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import PositiveTumbler
  import opened NatStrictTotalOrder
  import NatZeroMinimum
  import opened NatCarrierSet

  // First nonzero index from `start` onward in a tumbler with at least one
  // nonzero component in that range. This is the constructive least-element
  // witness from NAT-wellorder applied to the index set of nonzero positions.
  function FirstNonZero(t: Tumbler, start: nat): nat
    requires InT(t)
    requires 1 <= start <= Length(t)
    requires exists i :: start <= i <= Length(t) && Component(t, i) != 0
    ensures start <= FirstNonZero(t, start) <= Length(t)
    ensures Component(t, FirstNonZero(t, start)) != 0
    ensures forall j :: start <= j < FirstNonZero(t, start)
              ==> Component(t, j) == 0
    decreases Length(t) - start
  {
    if Component(t, start) != 0 then start
    else FirstNonZero(t, start + 1)
  }

  lemma PositiveDominatesZero(t: Tumbler, z: Tumbler)
    requires InT(t) && InT(z)
    requires PositiveTumbler.PositiveTumbler(t)
    requires PositiveTumbler.ZeroTumbler(z)
    ensures LexicographicOrder.LexicographicOrder(z, t)
  {
    var k := FirstNonZero(t, 1);

    if Length(z) >= k {
      // T1 case (i) with witness k.
      assert 1 <= k;
      assert k <= Length(z) && k <= Length(t);
      NatZeroMinimum.NatZeroMinimum(Component(t, k));
      assert Less(Component(z, k), Component(t, k));
      assert forall i :: 1 <= i < k ==>
        i <= Length(z) && i <= Length(t) &&
        Component(z, i) == Component(t, i);
      assert (k <= Length(z) && k <= Length(t) && Less(Component(z, k), Component(t, k)))
             || (k == Length(z) + 1 && k <= Length(t));
    } else {
      // T1 case (ii) with witness Length(z) + 1.
      var w: nat := Length(z) + 1;
      assert 1 <= w;
      assert w == Length(z) + 1 && w <= Length(t);
      assert forall i :: 1 <= i < w ==>
        i <= Length(z) && i <= Length(t) &&
        Component(z, i) == Component(t, i);
      assert (w <= Length(z) && w <= Length(t) && Less(Component(z, w), Component(t, w)))
             || (w == Length(z) + 1 && w <= Length(t));
    }
  }
}
