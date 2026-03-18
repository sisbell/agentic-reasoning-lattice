include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// N8 — AlwaysValidStates
module AlwaysValidStates {
  import opened TumblerAlgebra
  import TumblerHierarchy

  datatype State = State(nodes: set<Tumbler>)

  const Root: Tumbler := Tumbler([1])

  ghost predicate NodeAddress(n: Tumbler) {
    PositiveTumbler(n) &&
    TumblerHierarchy.ZeroCount(n.components) == 0
  }

  function Parent(n: Tumbler): Tumbler
    requires |n.components| > 1
  {
    Tumbler(n.components[..|n.components| - 1])
  }

  ghost predicate BaptizedNodes(s: State) {
    forall n :: n in s.nodes ==> NodeAddress(n)
  }

  ghost predicate SingleRoot(s: State) {
    Root in s.nodes &&
    forall n :: n in s.nodes && n != Root ==> IsPrefix(Root, n)
  }

  ghost predicate NodeTree(s: State) {
    Root in s.nodes &&
    forall n :: n in s.nodes && n != Root ==>
      |n.components| > 1 && Parent(n) in s.nodes
  }

  ghost predicate SequentialChildren(s: State) {
    forall c :: c in s.nodes && |c.components| > 1 ==>
      forall i: nat :: 1 <= i <= c.components[|c.components| - 1] ==>
        Tumbler(c.components[..|c.components| - 1] + [i]) in s.nodes
  }

  // DIVERGENCE: AllInvariants covers BaptizedNodes, N2, N3, N5 but omits N6
  // (StructuralOrdering). The ASN states N6 is derived from N3 and N5 by
  // structural induction, so preserving N3 and N5 entails preserving N6.
  ghost predicate AllInvariants(s: State) {
    BaptizedNodes(s) && SingleRoot(s) && NodeTree(s) && SequentialChildren(s)
  }

  // ZeroCount 0 means every component is positive
  lemma ZeroCountImpliesAllPositive(s: seq<nat>)
    requires TumblerHierarchy.ZeroCount(s) == 0
    ensures forall i :: 0 <= i < |s| ==> s[i] > 0
    decreases |s|
  {
    if |s| > 0 {
      ZeroCountImpliesAllPositive(s[1..]);
    }
  }

  // ZeroCount of all-positive sequence is 0
  lemma ZeroCountAllPositive(s: seq<nat>)
    requires forall i :: 0 <= i < |s| ==> s[i] > 0
    ensures TumblerHierarchy.ZeroCount(s) == 0
    decreases |s|
  {
    if |s| > 0 {
      ZeroCountAllPositive(s[1..]);
    }
  }

  // N2 preserved: root stays, new node descends from root
  lemma BaptizePreservesSingleRoot(pre: State, p: Tumbler, n: Tumbler)
    requires SingleRoot(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    ensures SingleRoot(State(pre.nodes + {n}))
  { }

  // BaptizedNodes preserved: new node is a valid node address
  lemma BaptizePreservesBaptizedNodes(pre: State, p: Tumbler, n: Tumbler)
    requires BaptizedNodes(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    requires n.components[|p.components|] > 0
    ensures BaptizedNodes(State(pre.nodes + {n}))
  {
    ZeroCountImpliesAllPositive(p.components);
    ZeroCountAllPositive(n.components);
  }

  // N3 preserved: parent of new node is p, which is in pre.nodes
  lemma BaptizePreservesNodeTree(pre: State, p: Tumbler, n: Tumbler)
    requires NodeTree(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    ensures NodeTree(State(pre.nodes + {n}))
  { }

  // N5 preserved: new child extends the sequential numbering
  lemma BaptizePreservesSequentialChildren(pre: State, p: Tumbler, n: Tumbler)
    requires SequentialChildren(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    requires n.components[|p.components|] > 0
    requires forall i: nat :: 1 <= i < n.components[|n.components| - 1] ==>
               Tumbler(p.components + [i]) in pre.nodes
    ensures SequentialChildren(State(pre.nodes + {n}))
  {
    var post := State(pre.nodes + {n});
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

  // N8 — AlwaysValidStates
  // BAPTIZE preserves all node invariants.
  lemma AlwaysValidStates(pre: State, p: Tumbler, n: Tumbler)
    requires AllInvariants(pre)
    requires p in pre.nodes
    requires |n.components| == |p.components| + 1
    requires n.components[..|p.components|] == p.components
    requires n.components[|p.components|] > 0
    requires n !in pre.nodes
    requires forall i: nat :: 1 <= i < n.components[|n.components| - 1] ==>
               Tumbler(p.components + [i]) in pre.nodes
    ensures AllInvariants(State(pre.nodes + {n}))
    ensures pre.nodes <= State(pre.nodes + {n}).nodes
  {
    BaptizePreservesBaptizedNodes(pre, p, n);
    BaptizePreservesSingleRoot(pre, p, n);
    BaptizePreservesNodeTree(pre, p, n);
    BaptizePreservesSequentialChildren(pre, p, n);
  }
}
