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

  // Postcondition (3): cross-param ordering — param-2 reach precedes param-1 reach under T1.
  // For any b extending p with b_{#p+1} = 0 and any a extending p with a_{#p+1} ≥ 1: b < a.
  // This captures the T1 case (i) argument at position #p+1.
  lemma CrossParamOrdering(p: Tumbler, a: Tumbler, b: Tumbler)
    requires InT(p) && InT(a) && InT(b)
    requires PrefixOf(p, a) && PrefixOf(p, b)
    requires Length(a) > Length(p)
    requires Length(b) > Length(p)
    requires Component(a, Length(p) + 1) >= 1
    requires Component(b, Length(p) + 1) == 0
    ensures LexicographicOrder.LexicographicOrder(b, a)
  {
    // T1 case (i): witness k = #p + 1.
    // Positions 1..#p: b_i = p_i = a_i (PrefixOf). Position k: b_k = 0 < 1 ≤ a_k.
    var k := Length(p) + 1;
    assert k <= Length(b) && k <= Length(a);
    assert Component(b, k) == 0;
    assert Component(a, k) >= 1;
    assert Component(b, k) < Component(a, k);
    assert forall i :: 1 <= i < k ==>
      i <= Length(b) && i <= Length(a) &&
      Component(b, i) == Component(a, i);
  }
}
