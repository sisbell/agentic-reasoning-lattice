// ASN-0034: PartitionMonotonicity (INV)
// For two sibling sub-partition prefixes p1 < p2 (non-nesting),
// every address extending p1 precedes every address extending p2 under T1.
include "./CarrierSetDefinition.dfy"
include "./PrefixRelation.dfy"
include "./LexicographicOrder.dfy"
include "./PrefixOrderingExtension.dfy"

module PartitionMonotonicity {
  import opened CarrierSetDefinition
  import opened NatCarrierSet
  import opened PrefixRelation
  import opened LexicographicOrder
  import POE = PrefixOrderingExtension

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
}
