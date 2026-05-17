// ASN-0034: T9 — ForwardAllocation (LEMMA)
// Within a single allocator's sequential stream, new addresses are
// strictly monotonically increasing under T1:
//   (A a, b : same_allocator(a, b) ∧ allocated_before(a, b) : a < b)
// Reduces directly to T10a.7 StrictMonotonicity at indices (i, j) with i < j.
include "./AllocatorDiscipline.dfy"
include "./CarrierSetDefinition.dfy"
include "./LexicographicOrder.dfy"
include "./EnumerationInjectivity.dfy"

module ForwardAllocation {
  import opened AllocatorDiscipline
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened LexicographicOrder
  import opened EnumerationInjectivity

  // allocated_before(a, b) ≡ a = tᵢ ∧ b = tⱼ ∧ i < j in some conforming
  // allocator's enumeration. By T10a.6 (DomainDisjointness) and T10a.7
  // (EnumerationInjectivity), the witnessing (A, i, j) is uniquely
  // determined on pairs satisfying same_allocator(a, b).
  ghost predicate AllocatedBefore(a: Tumbler, b: Tumbler) {
    exists A: Allocator, i: nat, j: nat ::
      AllocatorDiscipline.AllocatorDiscipline(A)
      && SiblingAt(A, i) == a
      && SiblingAt(A, j) == b
      && i < j
  }

  // T9 — earlier-allocated addresses are strictly less than later ones
  // under T1, within a single allocator's stream.
  lemma ForwardAllocation(a: Tumbler, b: Tumbler)
    requires SameAllocator(a, b)
    requires AllocatedBefore(a, b)
    ensures InT(a) && InT(b)
    ensures LexicographicOrder.LexicographicOrder(a, b)
  {
    var A: Allocator, i: nat, j: nat :|
      AllocatorDiscipline.AllocatorDiscipline(A)
      && SiblingAt(A, i) == a
      && SiblingAt(A, j) == b
      && i < j;
    StrictMonotonicity(A, i, j);
  }
}
