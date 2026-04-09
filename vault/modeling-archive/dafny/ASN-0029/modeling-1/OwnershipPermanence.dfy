include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module OwnershipPermanence {
  import opened TumblerAlgebra
  import opened Foundation

  // D3 encoding: account() is a pure function of address alone.
  // Bodyless = uninterpreted; captures "computable from d's tumbler
  // address alone, without consulting any mutable state."
  function Account(d: DocId): Tumbler

  // D2 — DocumentPermanence (transition invariant)
  ghost predicate DocumentPermanence(s: State, s': State) {
    forall d :: d in s.docs ==> d in s'.docs
  }

  // D3 — StructuralOwnership: state-level owner agrees with Account
  ghost predicate StructuralOwnership(owner: map<DocId, Tumbler>, docs: set<DocId>) {
    forall d :: d in docs ==> d in owner && owner[d] == Account(d)
  }

  // D4 — OwnershipPermanence (LEMMA)
  // Derived from D2 and D3.
  // For any document in the pre-state, its owner is identical in both states.
  //   owner[d] == Account(d)   (D3 on s)
  //   d in s'.docs             (D2)
  //   owner'[d] == Account(d)  (D3 on s')
  lemma OwnershipPermanence(
    s: State, s': State,
    owner: map<DocId, Tumbler>,
    owner': map<DocId, Tumbler>,
    d: DocId
  )
    requires DocumentPermanence(s, s')
    requires StructuralOwnership(owner, s.docs)
    requires StructuralOwnership(owner', s'.docs)
    requires d in s.docs
    ensures owner[d] == owner'[d]
  { }
}
