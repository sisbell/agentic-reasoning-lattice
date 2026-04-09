include "./PrefixOrderingExtension.dfy"
include "./ForwardAllocation.dfy"

module PartitionMonotonicity {
  // PartitionMonotonicity — INV
  // Full invariant: within any prefix-delimited partition, allocated addresses
  // are totally ordered by T1 consistently with per-allocator allocation order.
  // Postcondition (1): cross-partition ordering via PrefixOrderingExtension.
  // Postcondition (2): intra-partition allocation-order consistency via ForwardAllocation.
  // Invariant: structural induction over nested allocator partitions.

  import opened CarrierSetDefinition
  import opened LexicographicOrder
  import POE = PrefixOrderingExtension
  import FA = ForwardAllocation

  ghost predicate AllExtend(stream: seq<Tumbler>, p: Tumbler) {
    forall i :: 0 <= i < |stream| ==> POE.IsPrefix(p, stream[i])
  }

  ghost predicate NonNesting(p1: Tumbler, p2: Tumbler) {
    !POE.IsPrefix(p1, p2) && !POE.IsPrefix(p2, p1)
  }

  // ---- Postcondition (1): Cross-partition ordering ----

  // For sibling sub-partition prefixes p1 < p2 with neither a prefix of
  // the other, every extension of p1 precedes every extension of p2.
  ghost predicate PartitionMonotonicity(
    p1: Tumbler, p2: Tumbler,
    stream1: seq<Tumbler>, stream2: seq<Tumbler>
  ) {
    (LessThan(p1, p2) && NonNesting(p1, p2) &&
     AllExtend(stream1, p1) && AllExtend(stream2, p2))
    ==>
    forall i, j :: 0 <= i < |stream1| && 0 <= j < |stream2|
      ==> LessThan(stream1[i], stream2[j])
  }

  lemma PartitionMonotonicityHolds(
    p1: Tumbler, p2: Tumbler,
    stream1: seq<Tumbler>, stream2: seq<Tumbler>
  )
    requires LessThan(p1, p2)
    requires NonNesting(p1, p2)
    requires AllExtend(stream1, p1)
    requires AllExtend(stream2, p2)
    ensures forall i, j :: 0 <= i < |stream1| && 0 <= j < |stream2|
              ==> LessThan(stream1[i], stream2[j])
  {
    forall i, j | 0 <= i < |stream1| && 0 <= j < |stream2|
      ensures LessThan(stream1[i], stream2[j])
    {
      POE.PrefixOrderingExtension(p1, p2, stream1[i], stream2[j]);
    }
  }

  // ---- Postcondition (2): Intra-partition allocation-order consistency ----

  // Within a sub-partition with prefix t, the allocator produces addresses
  // via inc(·, 0). Allocation order is modeled as position in the allocator
  // stream: allocated_before(a, b) iff a = AllocatorStream(base, i) and
  // b = AllocatorStream(base, j) with i < j.
  // T9 (ForwardAllocation): i < j ⟹ AllocatorStream(base, i) < AllocatorStream(base, j).
  ghost predicate IntraPartitionConsistency(base: Tumbler, n: nat)
    requires ValidTumbler(base)
  {
    forall i, j :: 0 <= i < j <= n ==>
      LessThan(FA.AllocatorStream(base, i), FA.AllocatorStream(base, j))
  }

  lemma IntraPartitionConsistencyHolds(base: Tumbler, n: nat)
    requires ValidTumbler(base)
    ensures IntraPartitionConsistency(base, n)
  {
    forall i, j | 0 <= i < j <= n
      ensures LessThan(FA.AllocatorStream(base, i), FA.AllocatorStream(base, j))
    {
      FA.ForwardAllocation(base, i, j);
    }
  }

  // ---- Invariant: Total ordering within a prefix-delimited partition ----

  // A partition tree models the nested allocator structure within a
  // prefix-delimited partition (T10a). Leaf: single allocated address
  // (nesting depth 0). Node: root prefix + ordered sub-partitions,
  // each headed by a child allocator's sibling prefix.
  datatype PartitionTree =
    | PTLeaf(prefix: Tumbler)
    | PTNode(prefix: Tumbler, children: seq<PartitionTree>)

  function TreePrefix(t: PartitionTree): Tumbler {
    match t
    case PTLeaf(p) => p
    case PTNode(p, _) => p
  }

  // Collect all addresses from the tree in partition order.
  function TreeAddresses(t: PartitionTree): seq<Tumbler>
    decreases t
  {
    match t
    case PTLeaf(p) => [p]
    case PTNode(p, children) => [p] + ChildrenAddresses(children)
  }

  function ChildrenAddresses(children: seq<PartitionTree>): seq<Tumbler>
    decreases children
  {
    if |children| == 0 then []
    else TreeAddresses(children[0]) + ChildrenAddresses(children[1..])
  }

  // All addresses in a subtree extend its prefix.
  ghost predicate SubtreeExtends(t: PartitionTree)
    decreases t
  {
    var addrs := TreeAddresses(t);
    var p := TreePrefix(t);
    forall i :: 0 <= i < |addrs| ==> POE.IsPrefix(p, addrs[i])
  }

  // Well-formedness of a partition tree per T10a:
  // (1) Each child prefix extends the parent with strictly greater length
  // (2) Child prefixes are non-nesting and T1-ordered (sibling stream)
  // (3) Each child's addresses extend its prefix
  // (4) Recursive well-formedness
  ghost predicate WellFormedPartition(t: PartitionTree)
    decreases t
  {
    match t
    case PTLeaf(_) => true
    case PTNode(p, children) =>
      |children| >= 1 &&
      (forall i :: 0 <= i < |children| ==>
        POE.IsPrefix(p, TreePrefix(children[i])) &&
        |TreePrefix(children[i]).components| > |p.components|) &&
      (forall i, j :: 0 <= i < j < |children| ==>
        LessThan(TreePrefix(children[i]), TreePrefix(children[j])) &&
        NonNesting(TreePrefix(children[i]), TreePrefix(children[j]))) &&
      (forall i :: 0 <= i < |children| ==>
        SubtreeExtends(children[i])) &&
      (forall i :: 0 <= i < |children| ==>
        WellFormedPartition(children[i]))
  }

  // Tree-structured ordering: the invariant decomposed into its three parts
  // without flattening into a sequence. This avoids index arithmetic over
  // concatenated sequences while faithfully encoding the structural induction.
  ghost predicate TreeOrdered(t: PartitionTree)
    decreases t
  {
    match t
    case PTLeaf(_) => true
    case PTNode(p, children) =>
      // (a) Root precedes all addresses in every child subtree
      (forall ci, i :: 0 <= ci < |children| &&
        0 <= i < |TreeAddresses(children[ci])| ==>
        LessThan(p, TreeAddresses(children[ci])[i])) &&
      // (b) Cross-child ordering: addresses in earlier children precede
      //     addresses in later children (PrefixOrderingExtension)
      (forall ci, cj, i, j ::
        0 <= ci < cj < |children| &&
        0 <= i < |TreeAddresses(children[ci])| &&
        0 <= j < |TreeAddresses(children[cj])| ==>
        LessThan(TreeAddresses(children[ci])[i],
                 TreeAddresses(children[cj])[j])) &&
      // (c) Each child subtree is internally ordered (structural induction)
      (forall ci :: 0 <= ci < |children| ==> TreeOrdered(children[ci]))
  }

  // The full invariant: a well-formed partition tree is totally ordered.
  ghost predicate PartitionInvariant(t: PartitionTree) {
    (WellFormedPartition(t) && SubtreeExtends(t)) ==> TreeOrdered(t)
  }

  // Helper: proper prefix implies LessThan (T1 case ii).
  lemma ProperPrefixLessThan(p: Tumbler, q: Tumbler)
    requires POE.IsPrefix(p, q)
    requires |p.components| < |q.components|
    ensures LessThan(p, q)
  {
    LessThanTrichotomy(p, q);
  }

  // Helper: prefix transitivity — if p ≼ q and q ≼ r then p ≼ r.
  lemma PrefixTransitive(p: Tumbler, q: Tumbler, r: Tumbler)
    requires POE.IsPrefix(p, q)
    requires POE.IsPrefix(q, r)
    ensures POE.IsPrefix(p, r)
  {
  }

  // Helper: root precedes every address in a child subtree.
  lemma RootPrecedesSubtree(root: Tumbler, child: PartitionTree)
    requires POE.IsPrefix(root, TreePrefix(child))
    requires |TreePrefix(child).components| > |root.components|
    requires SubtreeExtends(child)
    ensures forall i :: 0 <= i < |TreeAddresses(child)| ==>
              LessThan(root, TreeAddresses(child)[i])
  {
    var addrs := TreeAddresses(child);
    var cp := TreePrefix(child);
    forall i | 0 <= i < |addrs|
      ensures LessThan(root, addrs[i])
    {
      assert POE.IsPrefix(cp, addrs[i]);
      PrefixTransitive(root, cp, addrs[i]);
      assert |addrs[i].components| >= |cp.components| > |root.components|;
      ProperPrefixLessThan(root, addrs[i]);
    }
  }

  // Main invariant lemma: structural induction on partition nesting depth.
  // Base case: single address (Leaf), trivially ordered.
  // Inductive step (Node): root < all descendants (ProperPrefixLessThan),
  //   cross-child ordering (PrefixOrderingExtension), within-child
  //   ordering (induction hypothesis).
  lemma PartitionInvariantHolds(t: PartitionTree)
    requires WellFormedPartition(t)
    requires SubtreeExtends(t)
    ensures TreeOrdered(t)
    decreases t
  {
    match t
    case PTLeaf(_) => {
      // Base case: single address, trivially ordered.
    }
    case PTNode(p, children) => {
      // (a) Root precedes all addresses in every child subtree.
      forall ci, i | 0 <= ci < |children| &&
        0 <= i < |TreeAddresses(children[ci])|
        ensures LessThan(p, TreeAddresses(children[ci])[i])
      {
        RootPrecedesSubtree(p, children[ci]);
      }

      // (b) Cross-child ordering via PrefixOrderingExtension.
      forall ci, cj, i, j |
        0 <= ci < cj < |children| &&
        0 <= i < |TreeAddresses(children[ci])| &&
        0 <= j < |TreeAddresses(children[cj])|
        ensures LessThan(TreeAddresses(children[ci])[i],
                         TreeAddresses(children[cj])[j])
      {
        var ai := TreeAddresses(children[ci])[i];
        var aj := TreeAddresses(children[cj])[j];
        assert POE.IsPrefix(TreePrefix(children[ci]), ai);
        assert POE.IsPrefix(TreePrefix(children[cj]), aj);
        POE.PrefixOrderingExtension(
          TreePrefix(children[ci]), TreePrefix(children[cj]), ai, aj);
      }

      // (c) Each child subtree is internally ordered by induction.
      forall ci | 0 <= ci < |children|
        ensures TreeOrdered(children[ci])
      {
        PartitionInvariantHolds(children[ci]);
      }
    }
  }
}
