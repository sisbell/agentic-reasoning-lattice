include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

// N3 — NodeTree
module NodeTree {
  import opened TumblerAlgebra

  datatype State = State(nodes: set<Tumbler>)

  const Root: Tumbler := Tumbler([1])

  // Parent of a node: drop the last component
  function Parent(n: Tumbler): Tumbler
    requires |n.components| > 1
  {
    Tumbler(n.components[..|n.components| - 1])
  }

  // N3 — NodeTree
  // The pair (Σ.nodes, parent) forms a finite tree rooted at r:
  // (a) r ∈ Σ.nodes
  // (b) (A n ∈ Σ.nodes : n ≠ r ⟹ parent(n) ∈ Σ.nodes)
  // (c) Σ.nodes is finite — Dafny's set<Tumbler> is finite by construction
  ghost predicate NodeTree(s: State) {
    Root in s.nodes &&
    forall n :: n in s.nodes && n != Root ==>
      |n.components| > 1 && Parent(n) in s.nodes
  }
}
