open util/ordering[Doc]

-- ═══════════════════════════════════════════════════════════════
-- D12 — VersionCreation (POST, ensures)
-- ASN-0029 · Document Ontology
--
-- Create a version (copy) of source document ds.  The version dv
-- receives a fresh address, an identical version list, and private
-- publication status.  Address allocation respects ordering
-- constraints (g1/g2) relative to account ownership.
-- ═══════════════════════════════════════════════════════════════

sig AccountAddr {}

sig Doc {
  account: one AccountAddr,
  parent:  lone Doc
}

sig Version {}
sig Link {}

abstract sig PubStatus {}
one sig Private, Published, Privashed extends PubStatus {}

sig State {
  D:   set Doc,
  V:   Doc -> set Version,
  pub: Doc -> lone PubStatus,
  I:   set Link
} {
  -- well-formedness: relations scoped to D
  V in D -> Version
  pub in D -> PubStatus
  all d: D | one pub[d]
}

----------------------------------------------------------------------
-- VersionCreation operation
----------------------------------------------------------------------

pred VersionCreation[s, sPost: State, ds, dv: Doc, aReq: AccountAddr] {
  -- ── PRE ──
  ds in s.D
  ds.account = aReq or s.pub[ds] in (Published + Privashed)

  -- ── POST (a): freshness ──
  dv not in s.D

  -- ── POST (b,c): version list copied ──
  sPost.V[dv] = s.V[ds]

  -- ── POST (d): source versions unchanged (subsumed by frame) ──

  -- ── POST (e): inclusions unchanged ──
  sPost.I = s.I

  -- ── POST (f): new doc is private ──
  sPost.pub[dv] = Private

  -- ── POST (g1): same account => dv after children of ds ──
  ds.account = aReq implies
    (all d2: s.D | d2.parent = ds implies lt[d2, dv])

  -- ── POST (g2): different account => dv after all of aReq's docs ──
  not (ds.account = aReq) implies
    (all d2: s.D | d2.account = aReq implies lt[d2, dv])

  -- ── FRAME ──
  sPost.D = s.D + dv
  all d2: s.D {
    sPost.V[d2]   = s.V[d2]
    sPost.pub[d2] = s.pub[d2]
  }
}

----------------------------------------------------------------------
-- Assertions
----------------------------------------------------------------------

-- Exactly one document is added
assert OnlyNewDocAdded {
  all s, sPost: State, ds, dv: Doc, aReq: AccountAddr |
    VersionCreation[s, sPost, ds, dv, aReq] implies
      sPost.D - s.D = dv
}

-- Source document remains in post-state
assert SourceInPostD {
  all s, sPost: State, ds, dv: Doc, aReq: AccountAddr |
    VersionCreation[s, sPost, ds, dv, aReq] implies
      ds in sPost.D
}

-- Existing documents' versions and pub status are unchanged
assert ExistingDocsUnchanged {
  all s, sPost: State, ds, dv: Doc, aReq: AccountAddr |
    VersionCreation[s, sPost, ds, dv, aReq] implies
      (all d: s.D | sPost.V[d] = s.V[d] and sPost.pub[d] = s.pub[d])
}

-- New doc is always private, even when source is published
assert NewDocAlwaysPrivate {
  all s, sPost: State, ds, dv: Doc, aReq: AccountAddr |
    VersionCreation[s, sPost, ds, dv, aReq] implies
      sPost.pub[dv] = Private
}

-- Inclusions are stable across version creation
assert InclusionsStable {
  all s, sPost: State, ds, dv: Doc, aReq: AccountAddr |
    VersionCreation[s, sPost, ds, dv, aReq] implies
      sPost.I = s.I
}

----------------------------------------------------------------------
-- Non-vacuity
----------------------------------------------------------------------

-- Same-account versioning with non-empty version list
run FindVersionCreation {
  some s, sPost: State, ds, dv: Doc, aReq: AccountAddr |
    VersionCreation[s, sPost, ds, dv, aReq]
    and some s.V[ds]
} for 5 but exactly 2 State

-- Cross-account versioning of a published doc
run FindCrossAccountVersion {
  some s, sPost: State, ds, dv: Doc, aReq: AccountAddr |
    VersionCreation[s, sPost, ds, dv, aReq]
    and not (ds.account = aReq)
    and some s.V[ds]
} for 5 but exactly 2 State, 2 AccountAddr

----------------------------------------------------------------------
-- Checks
----------------------------------------------------------------------

check OnlyNewDocAdded for 5 but exactly 2 State
check SourceInPostD for 5 but exactly 2 State
check ExistingDocsUnchanged for 5 but exactly 2 State
check NewDocAlwaysPrivate for 5 but exactly 2 State
check InclusionsStable for 5 but exactly 2 State
