// ASN-0034: TS1 — ShiftOrderPreservation
// (A v₁, v₂ ∈ T, n ∈ ℕ : n ≥ 1 ∧ #v₁ = #v₂ ∧ v₁ < v₂ :
//    shift(v₁, n) < shift(v₂, n))
include "./CarrierSetDefinition.dfy"
include "./PositiveTumbler.dfy"
include "./ActionPoint.dfy"
include "./LexicographicOrder.dfy"
include "./Divergence.dfy"
include "./OrdinalShift.dfy"
include "./OrdinalDisplacement.dfy"
include "./StrictOrderPreservation.dfy"
include "./TumblerAdd.dfy"
include "./NatStrictTotalOrder.dfy"

module ShiftOrderPreservation {
  import opened CarrierSetDefinition
  import opened PositiveTumbler
  import opened ActionPoint
  import opened LexicographicOrder
  import opened Divergence
  import opened OrdinalShift
  import opened OrdinalDisplacement
  import opened StrictOrderPreservation
  import opened TumblerAdd
  import opened NatStrictTotalOrder
  import opened NatCarrierSet

  lemma ShiftOrderPreservation(v1: Tumbler, v2: Tumbler, n: nat)
    requires InT(v1) && InT(v2)
    requires n >= 1
    requires Length(v1) == Length(v2)
    requires LexicographicOrder.LexicographicOrder(v1, v2)
    ensures LexicographicOrder.LexicographicOrder(
              OrdinalShift.OrdinalShift(v1, n),
              OrdinalShift.OrdinalShift(v2, n))
  {
    var m := Length(v1);
    var w := OrdinalDisplacement.OrdinalDisplacement(n, m);

    // From v1 < v2 and T1 irreflexivity, derive v1 != v2 to discharge
    // Divergence's precondition.
    StrictOrderPreservation.LexImpliesNotEqual(v1, v2);

    // Bound divergence(v1, v2) by m. Since #v1 = #v2 = m, if divergence
    // = m + 1 then all components agree, forcing v1 == v2 by Extensionality
    // — contradiction.
    var j := Divergence.Divergence(v1, v2);
    assert j == Divergence.FirstMismatch(v1, v2, 1, m);
    if j > m {
      assert j == m + 1;
      assert forall i :: 1 <= i <= m ==> Component(v1, i) == Component(v2, i);
      Extensionality(v1, v2);
      assert false;
    }
    assert 1 <= j <= m;

    // Discharge TA1-strict's preconditions with a = v1, b = v2, w = δ(n, m).
    assert ActionPoint.ActionPoint(w) == m;
    StrictOrderPreservation.StrictOrderPreservation(v1, v2, w);
  }
}
