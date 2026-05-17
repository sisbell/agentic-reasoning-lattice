// ASN-0034: TS5 — ShiftAmountMonotonicity
// Corollary: (A v ∈ T, n1, n2 : n1 >= 1 /\ n2 > n1 :
//              shift(v, n1) < shift(v, n2)).
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./OrdinalShift.dfy"
include "./ShiftComposition.dfy"
include "./ShiftStrictIncrease.dfy"

module ShiftAmountMonotonicity {
  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import OrdinalShift
  import ShiftComposition
  import ShiftStrictIncrease

  lemma ShiftAmountMonotonicity(v: Tumbler, n1: nat, n2: nat)
    requires InT(v)
    requires n1 >= 1
    requires n2 > n1
    ensures LexicographicOrder.LexicographicOrder(
              OrdinalShift.OrdinalShift(v, n1),
              OrdinalShift.OrdinalShift(v, n2))
  {
    var v1 := OrdinalShift.OrdinalShift(v, n1);
    var diff := n2 - n1;
    ShiftStrictIncrease.ShiftStrictIncrease(v1, diff);
    ShiftComposition.ShiftComposition(v, n1, diff);
  }
}
