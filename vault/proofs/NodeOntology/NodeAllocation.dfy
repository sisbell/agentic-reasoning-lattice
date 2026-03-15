// Node allocation properties (ASN-0035): N4, N8, N11, N12
// N15 (AllocationAuthority) and DC1 (AuthorityPermanence) deferred to Account Ontology.
module NodeAllocation {
  import opened TumblerAlgebra
  import opened NodeOntology
  import TumblerHierarchy
  import TumblerAllocation
  import NI = NodeIdentity

  // ---------------------------------------------------------------------------
  // N4 — BaptismMonotonicity
  // ---------------------------------------------------------------------------

  ghost predicate BaptismMonotonicity(pre: NodeState, post: NodeState) {
    pre.nodes <= post.nodes
  }

  // ---------------------------------------------------------------------------
  // N11 — CoordinationFreeDisjointness
  // ---------------------------------------------------------------------------

  lemma CoordinationFreeDisjointness(
    p1: Tumbler, p2: Tumbler,
    a: Tumbler, b: Tumbler
  )
    requires !IsPrefix(p1, p2) && !IsPrefix(p2, p1)
    requires IsPrefix(p1, a)
    requires IsPrefix(p2, b)
    ensures a != b
  {
    TumblerAllocation.PartitionIndependence(p1, p2, a, b);
  }

  // ---------------------------------------------------------------------------
  // N12 — LocalSerializationSufficiency
  // ---------------------------------------------------------------------------

  lemma UniqueParent(n: Tumbler, p: Tumbler, q: Tumbler)
    requires IsChildOf(n, p)
    requires IsChildOf(n, q)
    ensures p == q
  { }

  lemma DistinctParentsDistinctChildren(np: Tumbler, nq: Tumbler, p: Tumbler, q: Tumbler)
    requires p != q
    requires IsChildOf(np, p)
    requires IsChildOf(nq, q)
    ensures np != nq
  { }

  lemma ChildrenUnchanged(p: Tumbler, q: Tumbler, nodes: set<Tumbler>, nq: Tumbler)
    requires p != q
    requires IsChildOf(nq, q)
    ensures Children(p, nodes + {nq}) == Children(p, nodes)
  { }

  lemma LocalSerializationSufficiency(
    p: Tumbler, q: Tumbler,
    nodes: set<Tumbler>,
    np: Tumbler, nq: Tumbler
  )
    requires p != q
    requires IsChildOf(np, p)
    requires IsChildOf(nq, q)
    requires np !in nodes
    requires nq !in nodes
    ensures Children(p, nodes + {nq}) == Children(p, nodes)
    ensures Children(q, nodes + {np}) == Children(q, nodes)
    ensures np != nq
    ensures nodes + {np} + {nq} == nodes + {nq} + {np}
  { }

  // ---------------------------------------------------------------------------
  // N8 — AlwaysValidStates (BAPTIZE preserves all invariants)
  // ---------------------------------------------------------------------------

  ghost predicate AllInvariants(s: NodeState) {
    NI.BaptizedNodes(s) && NI.SingleRoot(s) && NI.NodeTree(s) && NI.SequentialChildren(s)
  }

  lemma BaptizePreservesSingleRoot(pre: NodeState, p: Tumbler, n: Tumbler)
    requires NI.SingleRoot(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    ensures NI.SingleRoot(NodeState(pre.nodes + {n}))
  { }

  lemma BaptizePreservesBaptizedNodes(pre: NodeState, p: Tumbler, n: Tumbler)
    requires NI.BaptizedNodes(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    requires n.components[|p.components|] > 0
    ensures NI.BaptizedNodes(NodeState(pre.nodes + {n}))
  {
    ZeroCountImpliesAllPositive(p.components);
    ZeroCountAllPositive(n.components);
  }

  lemma BaptizePreservesNodeTree(pre: NodeState, p: Tumbler, n: Tumbler)
    requires NI.NodeTree(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    ensures NI.NodeTree(NodeState(pre.nodes + {n}))
  { }

  lemma BaptizePreservesSequentialChildren(pre: NodeState, p: Tumbler, n: Tumbler)
    requires NI.SequentialChildren(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    requires n.components[|p.components|] > 0
    requires forall i: nat :: 1 <= i < n.components[|n.components| - 1] ==>
               Tumbler(p.components + [i]) in pre.nodes
    ensures NI.SequentialChildren(NodeState(pre.nodes + {n}))
  {
    var post := NodeState(pre.nodes + {n});
    var m := n.components[|n.components| - 1];
    forall c | c in post.nodes && |c.components| > 1
      ensures forall i: nat :: 1 <= i <= c.components[|c.components| - 1] ==>
                Tumbler(c.components[..|c.components| - 1] + [i]) in post.nodes
    {
      if c in pre.nodes {
      } else {
        assert c == n;
        assert c.components[..|c.components| - 1] == p.components;
        assert n.components == p.components + [m];
        forall i: nat | 1 <= i <= m
          ensures Tumbler(p.components + [i]) in post.nodes
        {
          if i < m {
          } else {
            assert Tumbler(p.components + [m]) == n;
          }
        }
      }
    }
  }

  lemma AlwaysValidStates(pre: NodeState, p: Tumbler, n: Tumbler)
    requires AllInvariants(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    requires n.components[|p.components|] > 0
    requires n !in pre.nodes
    requires forall i: nat :: 1 <= i < n.components[|n.components| - 1] ==>
               Tumbler(p.components + [i]) in pre.nodes
    ensures AllInvariants(NodeState(pre.nodes + {n}))
    ensures pre.nodes <= NodeState(pre.nodes + {n}).nodes
  {
    BaptizePreservesBaptizedNodes(pre, p, n);
    BaptizePreservesSingleRoot(pre, p, n);
    BaptizePreservesNodeTree(pre, p, n);
    BaptizePreservesSequentialChildren(pre, p, n);
  }
}
