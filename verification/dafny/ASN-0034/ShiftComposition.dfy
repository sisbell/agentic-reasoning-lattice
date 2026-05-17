// ASN-0034: TS3 — ShiftComposition
// Two successive shifts compose into a single shift:
// shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂).
include "./CarrierSetDefinition.dfy"
include "./OrdinalShift.dfy"

module ShiftComposition {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import OrdinalShift

  lemma ShiftComposition(v: Tumbler, n1: nat, n2: nat)
    requires InT(v)
    requires n1 >= 1
    requires n2 >= 1
    ensures OrdinalShift.OrdinalShift(OrdinalShift.OrdinalShift(v, n1), n2)
            == OrdinalShift.OrdinalShift(v, n1 + n2)
  {
    Extensionality(
      OrdinalShift.OrdinalShift(OrdinalShift.OrdinalShift(v, n1), n2),
      OrdinalShift.OrdinalShift(v, n1 + n2));
  }
}
