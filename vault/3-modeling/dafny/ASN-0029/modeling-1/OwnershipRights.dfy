include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module OwnershipRightsModule {
  import opened TumblerAlgebra
  import opened Foundation

  // D3: Account is a pure function of the address (state-independent)
  function Account(d: DocId): Tumbler

  // ASN-0029 publication status
  datatype PubStatus = Private | Published | Privashed

  // DIVERGENCE: Foundation.State lacks publication status and associate lists
  // introduced by ASN-0029. DocState wraps it with these fields.
  datatype DocState = DocState(
    base: State,
    pub_status: map<DocId, PubStatus>,
    associates: map<DocId, set<Tumbler>>
  )

  // D5(a),(b),(d) — owner-exclusive operations:
  // content modification, link modification, address subdivision
  ghost predicate OwnerExclusive(d: DocId, actor: Tumbler) {
    actor == Account(d)
  }

  // D5(c) — visibility when private: owner or designated associate
  ghost predicate VisibilityRight(ds: DocState, d: DocId, accessor: Tumbler)
    requires d in ds.pub_status
    requires d in ds.associates
  {
    ds.pub_status[d] == Private ==>
      (accessor == Account(d) || accessor in ds.associates[d])
  }

  // D5 — OwnershipRights (INV, predicate(State, DocId))
  // normative
  //
  // DIVERGENCE: D5 constrains operations, not single states. The four
  // rights (a)-(d) restrict which actors may perform each operation
  // class. As predicate(State, DocId) we express the structural
  // prerequisite: ownership metadata exists and the authorization
  // checks (OwnerExclusive, VisibilityRight) are well-defined for d.
  // Operational enforcement is in D15 (OwnerExclusiveModification).
  ghost predicate OwnershipRights(ds: DocState, d: DocId) {
    d in ds.base.docs &&
    d in ds.pub_status &&
    d in ds.associates
  }
}
