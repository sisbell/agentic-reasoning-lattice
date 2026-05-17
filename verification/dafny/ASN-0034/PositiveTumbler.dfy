// ASN-0034: TA-Pos — PositiveTumbler
// Pos(t) iff at least one component of t is nonzero:
//   Pos(t) ⇔ (E i : 1 ≤ i ≤ #t : tᵢ ≠ 0).
// Zero(t) iff all components are zero:
//   Zero(t) ⇔ (A i : 1 ≤ i ≤ #t : tᵢ = 0).
// Z = {t ∈ T : Zero(t)}.
include "./CarrierSetDefinition.dfy"

module PositiveTumbler {
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  ghost predicate PositiveTumbler(t: Tumbler)
    requires InT(t)
  {
    exists i :: 1 <= i <= Length(t) && Component(t, i) != 0
  }

  ghost predicate ZeroTumbler(t: Tumbler)
    requires InT(t)
  {
    forall i :: 1 <= i <= Length(t) ==> Component(t, i) == 0
  }

  ghost function ZeroSet(): iset<Tumbler>
  {
    iset t | InT(t) && ZeroTumbler(t)
  }

  // Consequence: Pos(t) ⟺ ¬Zero(t), by DeMorgan duality of bounded quantifiers.
  lemma PosIffNotZero(t: Tumbler)
    requires InT(t)
    ensures PositiveTumbler(t) <==> !ZeroTumbler(t)
  {
  }
}
