include "./OrdinalShift.dfy"

module ShiftInjectivity {
  // TS2 — ShiftInjectivity
  // shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂

  import opened CarrierSetDefinition
  import OS = OrdinalShift

  lemma ShiftInjectivity(v1: Tumbler, v2: Tumbler, n: nat)
    requires ValidTumbler(v1)
    requires ValidTumbler(v2)
    requires n >= 1
    requires |v1.components| == |v2.components|
    ensures OS.OrdinalShift(v1, n) == OS.OrdinalShift(v2, n) ==> v1 == v2
  { }
}
