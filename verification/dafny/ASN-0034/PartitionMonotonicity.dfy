// ASN-0034: PartitionMonotonicity (INV)
// For two sibling sub-partition prefixes p1 < p2 (non-nesting),
// every address extending p1 precedes every address extending p2 under T1.
include "./CarrierSetDefinition.dfy"
include "./PrefixRelation.dfy"
include "./LexicographicOrder.dfy"
include "./PrefixOrderingExtension.dfy"
include "./ForwardAllocation.dfy"

module PartitionMonotonicity {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PrefixRelation
  import opened LexicographicOrder
  import POE = PrefixOrderingExtension
  import AD = AllocatorDiscipline
  import FA = ForwardAllocation

  ghost predicate PartitionMonotonicity(p1: Tumbler, p2: Tumbler,
                                         part1: set<Tumbler>, part2: set<Tumbler>)
    requires InT(p1) && InT(p2)
    requires LexicographicOrder.LexicographicOrder(p1, p2)
    requires !PrefixOf(p1, p2) && !PrefixOf(p2, p1)
    requires forall t :: t in part1 ==> InT(t) && PrefixOf(p1, t)
    requires forall t :: t in part2 ==> InT(t) && PrefixOf(p2, t)
  {
    forall a, b :: a in part1 && b in part2 ==>
      LexicographicOrder.LexicographicOrder(a, b)
  }

  lemma PartitionMonotonicityHolds(p1: Tumbler, p2: Tumbler,
                                    part1: set<Tumbler>, part2: set<Tumbler>)
    requires InT(p1) && InT(p2)
    requires LexicographicOrder.LexicographicOrder(p1, p2)
    requires !PrefixOf(p1, p2) && !PrefixOf(p2, p1)
    requires forall t :: t in part1 ==> InT(t) && PrefixOf(p1, t)
    requires forall t :: t in part2 ==> InT(t) && PrefixOf(p2, t)
    ensures PartitionMonotonicity(p1, p2, part1, part2)
  {
    forall a, b | a in part1 && b in part2
      ensures LexicographicOrder.LexicographicOrder(a, b)
    {
      POE.PrefixOrderingExtension(p1, p2, a, b);
    }
  }

  // Postcondition (2): per-allocator forward allocation implies T1 ordering.
  // allocated_before(a, b) ⟹ a < b, for any a, b from the same allocator stream.
  lemma PartitionForwardAllocation(a: Tumbler, b: Tumbler)
    requires FA.AllocatedBefore(a, b)
    ensures InT(a) && InT(b)
    ensures LexicographicOrder.LexicographicOrder(a, b)
  {
    var A: AD.Allocator, i: nat, j: nat :|
      AD.AllocatorDiscipline(A)
      && AD.SiblingAt(A, i) == a
      && AD.SiblingAt(A, j) == b
      && i < j;
    assert AD.InDomain(a, A);
    assert AD.InDomain(b, A);
    assert AD.SameAllocator(a, b);
    FA.ForwardAllocation(a, b);
  }
}
