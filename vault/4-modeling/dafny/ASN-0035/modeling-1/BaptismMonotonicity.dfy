// N4 — BaptismMonotonicity (INV, predicate(State, State))
// ASN-0035: Node Ontology

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module BaptismMonotonicity {
  import opened TumblerAlgebra

  datatype State = State(nodes: set<Tumbler>)

  // N4 — BaptismMonotonicity
  // (A σ, σ' : σ precedes σ' : Σ.nodes(σ) ⊆ Σ.nodes(σ'))
  ghost predicate BaptismMonotonicity(pre: State, post: State) {
    pre.nodes <= post.nodes
  }
}
