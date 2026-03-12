include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressProperties/HierarchicalParsing.dfy"

module VersionPlacement {
  import opened TumblerAlgebra
  import opened Foundation
  import HierarchicalParsing

  // D13 — VersionPlacement (POST, ensures)
  // For CREATENEWVERSION(d_s, a_req) creating d_v:
  //   own-account:   parent(d_v) = d_s
  //   cross-account: account(d_v) = a_req ∧ parent(d_v) undefined

  predicate ValidDocAddr(d: Tumbler) {
    HierarchicalParsing.CountZeros(d.components) == 2
  }

  function FirstZeroFrom(s: seq<nat>, i: nat): nat
    requires i <= |s|
    requires exists j :: i <= j < |s| && s[j] == 0
    ensures i <= FirstZeroFrom(s, i) < |s|
    ensures s[FirstZeroFrom(s, i)] == 0
    ensures forall j :: i <= j < FirstZeroFrom(s, i) ==> s[j] != 0
    decreases |s| - i
  {
    if s[i] == 0 then i
    else FirstZeroFrom(s, i + 1)
  }

  predicate HasAccountLevel(d: Tumbler) {
    (exists j :: 0 <= j < |d.components| && d.components[j] == 0) &&
    FirstZeroFrom(d.components, 0) + 1 < |d.components|
  }

  function AccountPrefix(d: DocId): Tumbler
    requires HasAccountLevel(d)
  {
    var z := FirstZeroFrom(d.components, 0);
    Tumbler(d.components[..z+2])
  }

  ghost predicate DocLevelPrefix(ds: Tumbler, dv: Tumbler) {
    IsPrefix(ds, dv) && ds != dv &&
    ValidDocAddr(ds) && ValidDocAddr(dv)
  }

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
