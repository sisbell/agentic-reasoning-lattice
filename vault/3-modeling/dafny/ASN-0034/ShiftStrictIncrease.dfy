include "./StrictIncrease.dfy"
include "./OrdinalShift.dfy"

module ShiftStrictIncrease {
  // TS4 — ShiftStrictIncrease

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import OS = OrdinalShift
  import SI = StrictIncrease

  lemma ShiftStrictIncrease(v: Tumbler, n: nat)
    requires ValidTumbler(v)
    requires n >= 1
    ensures LessThan(v, OS.OrdinalShift(v, n))
  {
    var m := |v.components|;
    var delta := OS.Displacement(n, m);
    SI.StrictIncrease(v, delta);
  }
}
