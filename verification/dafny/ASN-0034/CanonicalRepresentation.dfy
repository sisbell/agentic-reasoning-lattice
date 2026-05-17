// ASN-0034: T3 — CanonicalRepresentation
// Tumbler equality is sequence equality:
//   a = b ⟺ #a = #b ∧ (∀ i ∈ ℕ : 1 ≤ i ≤ #a : aᵢ = bᵢ).
include "./CarrierSetDefinition.dfy"

module CanonicalRepresentation {
  import opened CarrierSetDefinition

  lemma CanonicalRepresentation(a: Tumbler, b: Tumbler)
    requires InT(a) && InT(b)
    ensures a == b <==>
      Length(a) == Length(b) &&
      forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i)
  {
    if Length(a) == Length(b) &&
       forall i :: 1 <= i <= Length(a) ==> Component(a, i) == Component(b, i) {
      Extensionality(a, b);
    }
  }
}
