// ASN-0034: T10 — PartitionIndependence
// If p₁, p₂ ∈ T with p₁ ⋠ p₂ ∧ p₂ ⋠ p₁, then for any a, b ∈ T with
// p₁ ≼ a and p₂ ≼ b, we have a ≠ b. The non-nesting prefixes locate
// a divergence index k ≤ min(#p₁, #p₂); PrefixOf transfers the
// component disagreement to a and b at that index.
include "./CarrierSetDefinition.dfy"
include "./PrefixRelation.dfy"

module PartitionIndependence {
  import opened CarrierSetDefinition
  import opened PrefixRelation
  import opened NatCarrierSet

  lemma PartitionIndependence(p1: Tumbler, p2: Tumbler, a: Tumbler, b: Tumbler)
    requires InT(p1) && InT(p2) && InT(a) && InT(b)
    requires !PrefixOf(p1, p2) && !PrefixOf(p2, p1)
    requires PrefixOf(p1, a) && PrefixOf(p2, b)
    ensures a != b
  { }
}
