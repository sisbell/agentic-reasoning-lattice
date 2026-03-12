include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressAllocation/HierarchicalParsing.dfy"
include "../../../../proofs/DocumentOntology/DocumentOntology.dfy"

module VersionPlacement {
  import opened TumblerAlgebra
  import opened Foundation
  import opened HierarchicalParsing
  import opened DocumentOntology

  // D13 — VersionPlacement (POST, ensures)
  // For CREATENEWVERSION(d_s, a_req) creating d_v:
  //   own-account:   parent(d_v) = d_s
  //   cross-account: account(d_v) = a_req ∧ parent(d_v) undefined

  // parent(d) = p in document set: p is max≼ doc-level prefix of c
  ghost predicate IsParentIn(p: DocId, c: DocId, docs: set<DocId>) {
    p in docs && DocLevelPrefix(p, c) &&
    forall d :: d in docs && DocLevelPrefix(d, c) ==>
      d == p || DocLevelPrefix(d, p)
  }

  // parent undefined: no doc-level prefix of d exists in docs
  ghost predicate NoParentIn(d: DocId, docs: set<DocId>) {
    forall d' :: d' in docs ==> !DocLevelPrefix(d', d)
  }

  ghost predicate VersionPlacement(
    ds: DocId,
    dv: DocId,
    aReq: IAddr,
    docs: set<DocId>
  )
    requires HasAccountLevel(ds)
    requires HasAccountLevel(dv)
  {
    ds in docs &&
    dv !in docs &&
    dv != ds &&
    ValidDocAddr(ds) &&
    ValidDocAddr(dv) &&
    // Own-account: parent(d_v) = d_s
    (AccountPrefix(ds) == aReq ==>
      IsParentIn(ds, dv, docs)) &&
    // Cross-account: account(d_v) = a_req, parent undefined
    (AccountPrefix(ds) != aReq ==>
      AccountPrefix(dv) == aReq &&
      NoParentIn(dv, docs))
  }
}
