// ASN-0034: TS2 — ShiftInjectivity
// Shift is injective over same-length tumblers: if shift(v1, n) = shift(v2, n)
// then v1 = v2.
include "./CarrierSetDefinition.dfy"
include "./OrdinalShift.dfy"

module ShiftInjectivity {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened OrdinalShift

  lemma ShiftInjectivity(v1: Tumbler, v2: Tumbler, n: nat)
    requires InT(v1) && InT(v2)
    requires n >= 1
    requires Length(v1) == Length(v2)
    requires OrdinalShift(v1, n) == OrdinalShift(v2, n)
    ensures v1 == v2
  {
    Extensionality(v1, v2);
  }
}
