// Shared definitions for node ontology (ASN-0035). Node addresses, tree
// structure, state, and helper lemmas used by all node property proofs.
module NodeOntology {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // ---------------------------------------------------------------------------
  // NodeAddress — a tumbler with all positive components (no zero separators)
  // ---------------------------------------------------------------------------

  ghost predicate NodeAddress(n: Tumbler) {
    PositiveTumbler(n) &&
    TumblerHierarchy.ZeroCount(n.components) == 0
  }

  // ---------------------------------------------------------------------------
  // Root — the single root node [1]
  // ---------------------------------------------------------------------------

  const Root: Tumbler := Tumbler([1])

  lemma RootIsNodeAddress()
    ensures NodeAddress(Root)
  {
    assert Root.components[0] != 0;
  }

  // ---------------------------------------------------------------------------
  // Parent — drop the last component
  // ---------------------------------------------------------------------------

  function Parent(n: Tumbler): Tumbler
    requires |n.components| > 1
  {
    Tumbler(n.components[..|n.components| - 1])
  }

  // ---------------------------------------------------------------------------
  // IsChildOf / Children — parent-child relations
  // ---------------------------------------------------------------------------

  ghost predicate IsChildOf(n: Tumbler, p: Tumbler) {
    |n.components| == |p.components| + 1 &&
    n.components[..|p.components|] == p.components
  }

  ghost function Children(p: Tumbler, nodes: set<Tumbler>): set<Tumbler> {
    set n | n in nodes && IsChildOf(n, p)
  }

  // ---------------------------------------------------------------------------
  // NodeContents — extensional node contents via prefix membership
  // ---------------------------------------------------------------------------

  ghost function NodeContents(n: Tumbler, addressSpace: set<Tumbler>): set<Tumbler> {
    set a | a in addressSpace && IsPrefix(n, a)
  }

  // ---------------------------------------------------------------------------
  // State
  // ---------------------------------------------------------------------------

  datatype NodeState = NodeState(nodes: set<Tumbler>)

  ghost predicate Genesis(s: NodeState) {
    s.nodes == {Root}
  }

  // ---------------------------------------------------------------------------
  // ZeroCount helper lemmas
  // ---------------------------------------------------------------------------

  lemma ZeroCountAllPositive(s: seq<nat>)
    requires forall i :: 0 <= i < |s| ==> s[i] > 0
    ensures TumblerHierarchy.ZeroCount(s) == 0
    decreases |s|
  {
    if |s| > 0 {
      ZeroCountAllPositive(s[1..]);
    }
  }

  lemma ZeroCountImpliesAllPositive(s: seq<nat>)
    requires TumblerHierarchy.ZeroCount(s) == 0
    ensures forall i :: 0 <= i < |s| ==> s[i] > 0
    decreases |s|
  {
    if |s| > 0 {
      ZeroCountImpliesAllPositive(s[1..]);
    }
  }
}
