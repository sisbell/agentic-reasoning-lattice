include "./PartitionMonotonicity.dfy"

module GlobalUniqueness {
  // GlobalUniqueness — INV (theorem from T1, T3, T4, T9, T10, T10a, TA5)
  // For every pair of addresses produced by distinct allocation events
  // in any reachable system state: a ≠ b.
  // Proof: PartitionMonotonicity establishes TreeOrdered (every pair ordered
  // by LessThan); T1 irreflexivity gives a < b ⟹ a ≠ b.

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import PM = PartitionMonotonicity

  // Bridge: LessThan implies distinct (from T1 irreflexivity)
  lemma LessThanImpliesDistinct(a: Tumbler, b: Tumbler)
    requires LessThan(a, b)
    ensures a != b
  {
    if a == b {
      LessThanIrreflexive(a);
    }
  }

  // Tree-structural uniqueness: no two distinct positions hold the same address.
  ghost predicate TreeUnique(t: PM.PartitionTree)
    decreases t
  {
    match t
    case PTLeaf(_) => true
    case PTNode(p, children) =>
      (forall ci, i ::
        (0 <= ci < |children| && 0 <= i < |PM.TreeAddresses(children[ci])|)
        ==> p != PM.TreeAddresses(children[ci])[i]) &&
      (forall ci, cj, i, j ::
        (0 <= ci < cj < |children| &&
         0 <= i < |PM.TreeAddresses(children[ci])| &&
         0 <= j < |PM.TreeAddresses(children[cj])|)
        ==> PM.TreeAddresses(children[ci])[i] != PM.TreeAddresses(children[cj])[j]) &&
      (forall ci :: 0 <= ci < |children| ==> TreeUnique(children[ci]))
  }

  // The invariant: well-formed partition ⟹ globally unique addresses.
  ghost predicate GlobalUniqueness(t: PM.PartitionTree) {
    (PM.WellFormedPartition(t) && PM.SubtreeExtends(t)) ==> TreeUnique(t)
  }

  // TreeOrdered ⟹ TreeUnique: ordering implies distinctness.
  lemma TreeOrderedImpliesUnique(t: PM.PartitionTree)
    requires PM.TreeOrdered(t)
    ensures TreeUnique(t)
    decreases t
  {
    match t
    case PTLeaf(_) => {}
    case PTNode(p, children) => {
      forall ci, i | 0 <= ci < |children| &&
        0 <= i < |PM.TreeAddresses(children[ci])|
        ensures p != PM.TreeAddresses(children[ci])[i]
      {
        LessThanImpliesDistinct(p, PM.TreeAddresses(children[ci])[i]);
      }
      forall ci, cj, i, j |
        0 <= ci < cj < |children| &&
        0 <= i < |PM.TreeAddresses(children[ci])| &&
        0 <= j < |PM.TreeAddresses(children[cj])|
        ensures PM.TreeAddresses(children[ci])[i] != PM.TreeAddresses(children[cj])[j]
      {
        LessThanImpliesDistinct(
          PM.TreeAddresses(children[ci])[i],
          PM.TreeAddresses(children[cj])[j]);
      }
      forall ci | 0 <= ci < |children|
        ensures TreeUnique(children[ci])
      {
        TreeOrderedImpliesUnique(children[ci]);
      }
    }
  }

  // Main theorem: well-formed partition trees have globally unique addresses.
  lemma GlobalUniquenessHolds(t: PM.PartitionTree)
    requires PM.WellFormedPartition(t)
    requires PM.SubtreeExtends(t)
    ensures TreeUnique(t)
  {
    PM.PartitionInvariantHolds(t);
    TreeOrderedImpliesUnique(t);
  }
}
