include "./OrdinalShift.dfy"
include "./CanonicalRepresentation.dfy"

module ShiftComposition {
  // TS3 — ShiftComposition
  // shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂)

  import opened CarrierSetDefinition
  import OS = OrdinalShift

  lemma ShiftComposition(v: Tumbler, n1: nat, n2: nat)
    requires ValidTumbler(v)
    requires n1 >= 1
    requires n2 >= 1
    ensures OS.OrdinalShift(OS.OrdinalShift(v, n1), n2) == OS.OrdinalShift(v, n1 + n2)
  { }
}
