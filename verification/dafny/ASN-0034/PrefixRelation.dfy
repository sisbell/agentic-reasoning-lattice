// ASN-0034: Prefix — PrefixRelation
// p ≼ q iff #p ≤ #q ∧ (∀i : 1 ≤ i ≤ #p : qᵢ = pᵢ).
// Proper prefix: p ≺ q iff p ≼ q ∧ p ≠ q.
include "./CarrierSetDefinition.dfy"

module PrefixRelation {
  import opened CarrierSetDefinition

  predicate PrefixOf(p: Tumbler, q: Tumbler)
    requires InT(p) && InT(q)
  {
    Length(p) <= Length(q) &&
    forall i :: 1 <= i <= Length(p) ==> Component(q, i) == Component(p, i)
  }

  predicate ProperPrefixOf(p: Tumbler, q: Tumbler)
    requires InT(p) && InT(q)
  {
    PrefixOf(p, q) && p != q
  }
}
