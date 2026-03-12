include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"
include "../../../../proofs/AddressAllocation/HierarchicalParsing.dfy"
include "../../../../proofs/DocumentOntology/DocumentOntology.dfy"

module VersionCreationModule {
  import opened TumblerAlgebra
  import opened Foundation
  import opened HierarchicalParsing
  import opened DocumentOntology

  // ASN-0029 D12 — VersionCreation (POST, ensures)
  // CREATENEWVERSION(d_s, a_req) → d_v

  // parent(d) = p in document set: p is the maximal doc-level prefix of d
  ghost predicate IsParentIn(p: DocId, c: DocId, docs: set<DocId>) {
    p in docs && DocLevelPrefix(p, c) &&
    forall d :: d in docs && DocLevelPrefix(d, c) ==>
      d == p || DocLevelPrefix(d, p)
  }

  // D12 specification: pre ∧ post ∧ frame
  ghost predicate VersionCreationSpec(
    s: DocState, s': DocState,
    ds: DocId, dv: DocId, aReq: IAddr
  ) {
    // ── PRE ──
    ds in s.base.docs &&
    ds in s.pub &&
    ValidDocAddr(ds) &&
    HasAccountLevel(ds) &&
    (s.pub[ds] == Published || s.pub[ds] == Privashed || AccountPrefix(ds) == aReq) &&
    // ── POST (a): freshness ──
    dv !in s.base.docs && dv in s'.base.docs &&
    ValidDocAddr(dv) &&
    // ── POST (b,c): V-space copied ──
    ds in s.base.vmap && dv in s'.base.vmap &&
    s'.base.vmap[dv] == s.base.vmap[ds] &&
    // (d) source V-space unchanged — subsumed by frame
    // ── POST (e): I-space unchanged ──
    s'.base.iota == s.base.iota &&
    // ── POST (f): new doc is private ──
    dv in s'.pub && s'.pub[dv] == Private &&
    // ── POST (g1): same-account — dv after children of ds ──
    (AccountPrefix(ds) == aReq ==>
      forall d' :: d' in s.base.docs && IsParentIn(ds, d', s.base.docs) ==>
        LessThan(d', dv)) &&
    // ── POST (g2): cross-account — dv after all of aReq's docs ──
    (AccountPrefix(ds) != aReq ==>
      forall d' :: (d' in s.base.docs && HasAccountLevel(d') &&
        AccountPrefix(d') == aReq) ==>
        LessThan(d', dv)) &&
    // ── FRAME ──
    s'.base.docs == s.base.docs + {dv} &&
    (forall d' :: (d' in s.base.docs && d' in s.base.vmap && d' in s.pub) ==>
      d' in s'.base.vmap && s'.base.vmap[d'] == s.base.vmap[d'] &&
      d' in s'.pub && s'.pub[d'] == s.pub[d'])
  }
}
