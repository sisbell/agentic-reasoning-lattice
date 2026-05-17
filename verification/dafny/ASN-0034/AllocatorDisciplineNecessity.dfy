// ASN-0034: T10a-N — AllocatorDisciplineNecessity (LEMMA)
// Relaxing T10a's sibling restriction to permit inc(·, k) with k > 0 in the
// sibling stream falsifies T10a.2 (NonNestingSiblingPrefixes). For any
// t₀ ∈ T and k > 0, the pair t₁ = inc(t₀, 0) and t₂ = inc(t₁, k) — co-sibling
// outputs under the relaxation — satisfies t₁ ≼ t₂ with t₁ ≠ t₂ by TA5(d)
// (length extension) and TA5(b) (agreement on positions 1..#t₁).
include "./CarrierSetDefinition.dfy"
include "./HierarchicalIncrement.dfy"
include "./PrefixRelation.dfy"

module AllocatorDisciplineNecessity {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened HierarchicalIncrement
  import opened PrefixRelation

  lemma AllocatorDisciplineNecessity(t0: Tumbler, k: nat)
    requires InT(t0)
    requires k > 0
    ensures
      var t1 := HierarchicalIncrement(t0, 0);
      InT(t1) &&
      var t2 := HierarchicalIncrement(t1, k);
      InT(t2) && PrefixOf(t1, t2) && t1 != t2
  {
  }
}
