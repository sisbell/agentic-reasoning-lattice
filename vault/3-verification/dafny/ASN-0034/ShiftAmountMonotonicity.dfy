include "./ShiftComposition.dfy"
include "./ShiftStrictIncrease.dfy"

module ShiftAmountMonotonicity {
  // TS5 — ShiftAmountMonotonicity
  // (A v, n1, n2 : n1 >= 1 /\ n2 > n1 : shift(v, n1) < shift(v, n2))
  // Corollary of TS3 (ShiftComposition) and TS4 (ShiftStrictIncrease)

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import OS = OrdinalShift
  import SC = ShiftComposition
  import SS = ShiftStrictIncrease

  lemma ShiftAmountMonotonicity(v: Tumbler, n1: nat, n2: nat)
    requires ValidTumbler(v)
    requires n1 >= 1
    requires n2 > n1
    ensures LessThan(OS.OrdinalShift(v, n1), OS.OrdinalShift(v, n2))
  {
    var v1 := OS.OrdinalShift(v, n1);
    var diff := n2 - n1;
    // TS4: v1 < shift(v1, diff)
    SS.ShiftStrictIncrease(v1, diff);
    // TS3: shift(v1, diff) == shift(v, n1 + diff) == shift(v, n2)
    SC.ShiftComposition(v, n1, diff);
  }
}
