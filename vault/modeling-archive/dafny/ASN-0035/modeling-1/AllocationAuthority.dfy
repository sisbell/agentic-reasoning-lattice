// N15 — AllocationAuthority (PRE, requires)
// ASN-0035: Node Ontology

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AllocationAuthority {
  import opened TumblerAlgebra

  // Actor identity — opaque type, refined by account ontology
  type Actor(==)

  datatype State = State(nodes: set<Tumbler>)

  // authorized(actor, p) — abstract predicate; refinement deferred to account ontology ASN
  ghost predicate {:axiom} authorized(actor: Actor, p: Tumbler)

  // N15 — AllocationAuthority
  // BAPTIZE(actor, p) precondition: p ∈ Σ.nodes ∧ authorized(actor, p)
  ghost predicate AllocationAuthorityPre(s: State, actor: Actor, p: Tumbler) {
    p in s.nodes && authorized(actor, p)
  }
}
