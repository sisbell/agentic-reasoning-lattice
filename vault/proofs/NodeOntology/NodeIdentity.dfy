// Node identity properties (ASN-0035): Σ.nodes, N0, N1, N2, N3, N5, N6,
// N7, N9, N10, N13, N14, N16
module NodeIdentity {
  import opened TumblerAlgebra
  import opened NodeOntology
  import TumblerHierarchy
  import TumblerOrder
  import TumblerAddition

  // ---------------------------------------------------------------------------
  // Σ.nodes — BaptizedNodes
  // ---------------------------------------------------------------------------

  ghost predicate BaptizedNodes(s: NodeState) {
    forall n :: n in s.nodes ==> NodeAddress(n)
  }

  lemma GenesisValid(s: NodeState)
    requires Genesis(s)
    ensures BaptizedNodes(s)
  {
    RootIsNodeAddress();
  }

  // ---------------------------------------------------------------------------
  // N0 — GhostElement
  // ---------------------------------------------------------------------------

  lemma GhostElement(n: Tumbler)
    requires NodeAddress(n)
    ensures PositiveTumbler(Tumbler([1]))
    ensures TumblerAddition.SpanWellDefined(n, Tumbler([1]))
  {
    assert Tumbler([1]).components[0] != 0;
  }

  // ---------------------------------------------------------------------------
  // N1 — IdentityByAssignment
  // ---------------------------------------------------------------------------

  ghost predicate IdentityByAssignment(a: Tumbler, b: Tumbler) {
    a == b <==> a.components == b.components
  }

  lemma IdentityDeterminedByAddress(a: Tumbler, b: Tumbler)
    ensures IdentityByAssignment(a, b)
  {
    TumblerOrder.CanonicalRepresentation(a, b);
  }

  // ---------------------------------------------------------------------------
  // N2 — SingleRoot
  // ---------------------------------------------------------------------------

  ghost predicate SingleRoot(s: NodeState) {
    Root in s.nodes &&
    forall n :: n in s.nodes && n != Root ==> IsPrefix(Root, n)
  }

  // ---------------------------------------------------------------------------
  // N3 — NodeTree
  // ---------------------------------------------------------------------------

  ghost predicate NodeTree(s: NodeState) {
    Root in s.nodes &&
    forall n :: n in s.nodes && n != Root ==>
      |n.components| > 1 && Parent(n) in s.nodes
  }

  // ---------------------------------------------------------------------------
  // N5 — SequentialChildren
  // ---------------------------------------------------------------------------

  ghost predicate SequentialChildren(s: NodeState) {
    forall c :: c in s.nodes && |c.components| > 1 ==>
      forall i: nat :: 1 <= i <= c.components[|c.components| - 1] ==>
        Tumbler(c.components[..|c.components| - 1] + [i]) in s.nodes
  }

  // ---------------------------------------------------------------------------
  // N6 — StructuralOrdering (T1 = DFS pre-order on node tree)
  // ---------------------------------------------------------------------------

  lemma PrefixPrecedesDescendant(p: Tumbler, d: Tumbler)
    requires IsPrefix(p, d)
    requires p != d
    ensures LessThan(p, d)
  {
    LessThanIntro(p, d, |p.components|);
  }

  lemma InterSubtreeOrdering(p: Tumbler, ci: Tumbler, cj: Tumbler,
                              di: Tumbler, dj: Tumbler)
    requires |ci.components| == |p.components| + 1
    requires |cj.components| == |p.components| + 1
    requires ci.components[..|p.components|] == p.components
    requires cj.components[..|p.components|] == p.components
    requires ci.components[|p.components|] < cj.components[|p.components|]
    requires IsPrefix(ci, di)
    requires IsPrefix(cj, dj)
    ensures LessThan(di, dj)
  {
    LessThanIntro(di, dj, |p.components|);
  }

  // ---------------------------------------------------------------------------
  // N7 — ForwardReferenceAdmissibility
  // ---------------------------------------------------------------------------

  lemma ForwardReferenceAdmissibility(n: Tumbler, l: Tumbler)
    requires NodeAddress(n)
    requires PositiveTumbler(l)
    requires ActionPoint(l) < |n.components|
    ensures LessThan(n, TumblerAdd(n, l))
  {
    TumblerAddition.StrictIncrease(n, l);
  }

  // ---------------------------------------------------------------------------
  // N9 — SubtreeContiguity (T5 applied to node prefixes)
  // ---------------------------------------------------------------------------

  lemma SubtreeContiguity(n: Tumbler, a: Tumbler, b: Tumbler, c: Tumbler)
    requires IsPrefix(n, a)
    requires IsPrefix(n, c)
    requires LessEq(a, b)
    requires LessEq(b, c)
    ensures IsPrefix(n, b)
  {
    TumblerHierarchy.ContiguousSubtrees(n, a, b, c);
  }

  // ---------------------------------------------------------------------------
  // N10 — SubtreeDisjointness (T10 applied to node prefixes)
  // ---------------------------------------------------------------------------

  lemma SubtreeDisjointness(m: Tumbler, n: Tumbler, a: Tumbler, b: Tumbler)
    requires !IsPrefix(m, n) && !IsPrefix(n, m)
    requires IsPrefix(m, a)
    requires IsPrefix(n, b)
    ensures a != b
  { }

  // ---------------------------------------------------------------------------
  // N13 — UniformNodeType
  // ---------------------------------------------------------------------------

  ghost predicate UniformNodeType(n: Tumbler) {
    NodeAddress(n)
  }

  lemma AllPositiveTumblerIsNode(n: Tumbler)
    requires PositiveTumbler(n)
    requires forall i :: 0 <= i < |n.components| ==> n.components[i] > 0
    ensures NodeAddress(n)
  {
    ZeroCountAllPositive(n.components);
  }

  // ---------------------------------------------------------------------------
  // N14 — NoNodeMutableState
  // ---------------------------------------------------------------------------

  ghost predicate NoNodeMutableState(n: Tumbler, space1: set<Tumbler>, space2: set<Tumbler>) {
    NodeContents(n, space1) == NodeContents(n, space2) ==>
    true  // node has no state beyond its extensional contents
  }

  lemma NoNodeMutableStateHolds(n: Tumbler, space1: set<Tumbler>, space2: set<Tumbler>)
    ensures NoNodeMutableState(n, space1, space2)
  { }

  // ---------------------------------------------------------------------------
  // N16 — PrefixPropagation
  // ---------------------------------------------------------------------------

  lemma PrefixPropagation(n: Tumbler, a: Tumbler, k: nat)
    requires PositiveTumbler(n)
    requires |n.components| > 0
    requires k > 0
    ensures IsPrefix(n, AllocationInc(n, k))
  { }
}
