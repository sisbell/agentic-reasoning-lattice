// ASN-0034: TA-Pos — PositiveTumbler
// Pos(t) iff at least one component of t is nonzero:
//   Pos(t) ⇔ (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0).
include "./CarrierSetDefinition.dfy"

module PositiveTumbler {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  ghost predicate PositiveTumbler(t: Tumbler)
    requires InT(t)
  {
    exists i :: 1 <= i <= Length(t) && Component(t, i) != 0
  }
}
