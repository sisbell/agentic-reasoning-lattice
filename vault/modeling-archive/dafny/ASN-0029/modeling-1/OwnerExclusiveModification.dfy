include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module OwnerExclusiveModificationModule {
  import opened TumblerAlgebra
  import opened Foundation

  // D3: account is a pure function of the address (state-independent)
  function Account(d: DocId): Tumbler

  // ASN-0029 D15 — OwnerExclusiveModification (INV, predicate(State, DocId))
  // [op modifies Σ.V(d) ⟹ account(d) = actor(op)]
  // Design requirement on correct participants.
  //
  // DIVERGENCE: predicate(State, DocId) cannot bind the actor (external to
  // the state). Added actor parameter. The predicate is the authorization
  // check that any operation modifying V(d) must satisfy as a precondition.
  ghost predicate OwnerExclusiveModification(s: State, d: DocId, actor: Tumbler)
    requires d in s.docs
    requires d in s.vmap
  {
    actor == Account(d)
  }
}
