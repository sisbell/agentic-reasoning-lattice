include "./OrdinalShift.dfy"

module ShiftOrderPreservation {
  // TS1 — ShiftOrderPreservation

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import OS = OrdinalShift

  lemma ShiftOrderPreservation(a: Tumbler, b: Tumbler, n: nat)
    requires ValidTumbler(a)
    requires ValidTumbler(b)
    requires |a.components| == |b.components|
    requires LessThan(a, b)
    requires n >= 1
    ensures LessThan(OS.OrdinalShift(a, n), OS.OrdinalShift(b, n))
  { }
}
