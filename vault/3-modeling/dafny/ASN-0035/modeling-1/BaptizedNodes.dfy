// Σ.nodes — BaptizedNodes (INV, predicate(State))
// ASN-0035: Node Ontology

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module BaptizedNodes {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // N = {n ∈ T : n > 0 ∧ zeros(n) = 0}
  ghost predicate NodeAddress(n: Tumbler) {
    PositiveTumbler(n) &&
    TumblerHierarchy.ZeroCount(n.components) == 0
  }

  datatype State = State(nodes: set<Tumbler>)

  const Root: Tumbler := Tumbler([1])

  // Σ.nodes ⊆ N
  ghost predicate BaptizedNodes(s: State) {
    forall n :: n in s.nodes ==> NodeAddress(n)
  }

  // Genesis: Σ.nodes = {r}
  ghost predicate Genesis(s: State) {
    s.nodes == {Root}
  }

  lemma RootIsNodeAddress()
    ensures NodeAddress(Root)
  {
    assert Root.components[0] != 0;
  }

  // Genesis satisfies BaptizedNodes
  lemma GenesisValid(s: State)
    requires Genesis(s)
    ensures BaptizedNodes(s)
  {
    RootIsNodeAddress();
  }
}
