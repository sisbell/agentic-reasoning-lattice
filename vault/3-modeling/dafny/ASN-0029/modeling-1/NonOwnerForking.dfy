include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module NonOwnerForkingModule {
  import opened TumblerAlgebra
  import opened Foundation

  datatype PubStatus = Private | Published | Privashed

  // D3: account is a pure function of the address (state-independent)
  function Account(d: DocId): Tumbler

  // ASN-0029 D16 — NonOwnerForking (INV, predicate(State, DocId))
  // behavioral invariant
  //
  // account(d) ≠ actor(op) ∧ op requests modification of d
  // ∧ (Σ.pub(d) ∈ {published, privashed})
  // ⟹ system applies CREATENEWVERSION(d, actor(op)) with account(d_v) = actor(op)
  //
  // DIVERGENCE: predicate(State, DocId) cannot express the transition
  // response (fork creation involves pre/post states and an actor). We
  // model D16 as a transition predicate with additional parameters for
  // actor and publication maps. The account function is bodyless (axiom)
  // per D3: account is computable from the address alone.
  ghost predicate NonOwnerForking(
    s: State, s': State,
    pub: map<DocId, PubStatus>, pub': map<DocId, PubStatus>,
    d: DocId,
    actor: Tumbler
  ) {
    // Trigger: non-owner requests modification of published/privashed doc
    (d in s.docs && d in pub &&
     Account(d) != actor &&
     (pub[d] == Published || pub[d] == Privashed))
    ==>
    // Response: system forks via CREATENEWVERSION(d, actor)
    (exists d_v: DocId ::
      // Fork is fresh
      d_v !in s.docs && d_v in s'.docs &&
      // Fork is owned by requesting actor
      Account(d_v) == actor &&
      // Fork starts private
      d_v in pub' && pub'[d_v] == Private &&
      // Original preserved
      d in s'.docs && d in pub' && pub'[d] == pub[d] &&
      // Only the fork is added
      s'.docs == s.docs + {d_v})
  }
}
