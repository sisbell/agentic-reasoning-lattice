// DC1 — AuthorityPermanence (INV, predicate(State, State))
// ASN-0035: Node Ontology

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module AuthorityPermanence {
  import opened TumblerAlgebra

  // Actor identity — opaque type, refined by account ontology
  type Actor(==)

  // Authorization grant — actor authorized to create children under node
  datatype AuthGrant = AuthGrant(actor: Actor, node: Tumbler)

  datatype State = State(authorized: set<AuthGrant>)

  // DC1 — AuthorityPermanence
  // Authority, once established, is irrevocable:
  // (A actor, p, σ : authorized(actor, p) in σ ⟹
  //   (A σ' : σ precedes σ' : authorized(actor, p) in σ'))
  // Design constraint: the account ontology must define state transitions
  // such that every transition preserves this predicate.
  ghost predicate AuthorityPermanence(pre: State, post: State) {
    pre.authorized <= post.authorized
  }
}
