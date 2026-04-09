-- D13-VersionPlacement.als
-- Property: VersionPlacement postcondition of CreateNewVersion
--
-- D13: For CreateNewVersion(d_s, a_req) creating d_v:
--   account(d_s) = a_req  =>  parent(d_v) = d_s
--   account(d_s) != a_req =>  account(d_v) = a_req and parent(d_v) undefined
--
-- Own-account: inc(d_s, 1), preserving zeros(d_v) = 2.
-- Cross-account: root allocator for a_req.

sig Account {}

sig Document {
  account: one Account,
  parent: lone Document
}

-- Hierarchical consistency: a child document belongs to the same account as its parent
fact AccountConsistency {
  all d: Document | some d.parent implies d.account = d.parent.account
}

-- No cycles in the parent chain
fact NoCycles {
  no d: Document | d in d.^parent
}

pred isRoot[d: Document] {
  no d.parent
}

-- D13 VersionPlacement: postcondition of CreateNewVersion
pred CreateNewVersion[ds, dv: Document, aReq: Account] {
  dv != ds

  -- Own-account: version placed as child of source
  ds.account = aReq implies dv.parent = ds

  -- Cross-account: version placed as root under requester's account
  ds.account != aReq implies (dv.account = aReq and no dv.parent)
}

-- Derived property: the version always ends up in the requester's account
assert VersionBelongsToRequester {
  all ds, dv: Document, aReq: Account |
    CreateNewVersion[ds, dv, aReq] implies dv.account = aReq
}

-- Cross-account versioning produces a root document
assert CrossAccountCreatesRoot {
  all ds, dv: Document, aReq: Account |
    (CreateNewVersion[ds, dv, aReq] and ds.account != aReq)
      implies isRoot[dv]
}

-- Own-account versioning makes source the parent of the version
assert OwnAccountSourceIsParent {
  all ds, dv: Document, aReq: Account |
    (CreateNewVersion[ds, dv, aReq] and ds.account = aReq)
      implies dv.parent = ds
}

-- Non-vacuity: own-account version creation
run FindOwnAccount {
  some ds, dv: Document, aReq: Account |
    CreateNewVersion[ds, dv, aReq] and ds.account = aReq
} for 4 but exactly 2 Document

-- Non-vacuity: cross-account version creation
run FindCrossAccount {
  some ds, dv: Document, aReq: Account |
    CreateNewVersion[ds, dv, aReq] and ds.account != aReq
} for 4 but exactly 2 Document, exactly 2 Account

check VersionBelongsToRequester for 5
check CrossAccountCreatesRoot for 5
check OwnAccountSourceIsParent for 5
