// ASN-0034: T10a.1 — UniformSiblingLength (LEMMA, corollary)
// All siblings produced by a single allocator share the same length as
// the base address. Sibling production uses only inc(·, 0), which by
// TA5(c) preserves length, so the entire stream is length-uniform.
include "./AllocatorDiscipline.dfy"
include "./HierarchicalIncrement.dfy"
include "./CarrierSetDefinition.dfy"

module UniformSiblingLength {
  import opened AllocatorDiscipline
  import opened HierarchicalIncrement
  import opened CarrierSetDefinition
  import opened NatCarrierSet

  lemma SiblingInT(a: Allocator, n: nat)
    requires AllocatorDiscipline(a)
    ensures InT(SiblingAt(a, n))
    decreases n
  {
    if n == 0 {
    } else {
      SiblingInT(a, n - 1);
    }
  }

  lemma UniformSiblingLength(a: Allocator, n: nat)
    requires AllocatorDiscipline(a)
    ensures Length(SiblingAt(a, n)) == Length(BaseAddress(a))
    decreases n
  {
    if n == 0 {
    } else {
      UniformSiblingLength(a, n - 1);
      SiblingInT(a, n - 1);
    }
  }
}
