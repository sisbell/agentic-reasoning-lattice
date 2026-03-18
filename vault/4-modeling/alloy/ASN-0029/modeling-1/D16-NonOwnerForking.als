-- D16 — NonOwnerForking (INV, predicate(State, DocId))
-- ASN-0029 · Document Ontology
--
-- account(d) ≠ actor(op) ∧ op requests modification of d
-- ∧ (Σ.pub(d) ∈ {published, privashed})
-- ⟹ system applies CREATENEWVERSION(d, actor(op))
--    with account(d_v) = actor(op)
--
-- When a non-owner requests modification of a published or privashed
-- document, the system forks: CREATENEWVERSION produces a new version
-- owned by the requesting actor rather than modifying the original.

sig AccountAddr {}

sig Doc {
  account: one AccountAddr
}

sig Content {}

abstract sig PubStatus {}
one sig Private, Published, Privashed extends PubStatus {}

sig State {
  D:   set Doc,
  val: Doc -> lone Content,
  pub: Doc -> lone PubStatus
} {
  val in D -> Content
  pub in D -> PubStatus
  all d: D | one pub[d]
}

----------------------------------------------------------------------
-- NonOwnerFork: system response to non-owner modify request
----------------------------------------------------------------------

pred NonOwnerFork[s, sPost: State, actor: AccountAddr, d, dv: Doc] {
  -- ── PRE ──
  d in s.D
  d.account != actor
  s.pub[d] in Published + Privashed

  -- ── POST: new version is fresh, owned by actor ──
  dv not in s.D
  dv.account = actor

  -- ── POST: new version starts private ──
  sPost.pub[dv] = Private

  -- ── POST: new version gets a copy of the content ──
  sPost.val[dv] = s.val[d]

  -- ── FRAME ──
  sPost.D = s.D + dv
  all d2: s.D {
    sPost.val[d2] = s.val[d2]
    sPost.pub[d2] = s.pub[d2]
  }
}

----------------------------------------------------------------------
-- Unconstrained modification (no ownership guard, no forking)
----------------------------------------------------------------------

pred UnconstrainedModify[s, sPost: State, actor: AccountAddr,
                         d: Doc, c: Content] {
  d in s.D
  not (s.val[d] = c)
  sPost.val[d] = c
  sPost.D = s.D
  all d2: s.D - d | sPost.val[d2] = s.val[d2]
  sPost.pub = s.pub
}

----------------------------------------------------------------------
-- Assertions
----------------------------------------------------------------------

-- D16a: The forked version is owned by the requesting actor
assert ForkOwnership {
  all s, sPost: State, actor: AccountAddr, d, dv: Doc |
    NonOwnerFork[s, sPost, actor, d, dv]
    implies dv.account = actor
}

-- D16b: The forked version is NOT owned by the original's owner
assert ForkChangesOwnership {
  all s, sPost: State, actor: AccountAddr, d, dv: Doc |
    NonOwnerFork[s, sPost, actor, d, dv]
    implies dv.account != d.account
}

-- D16c: The original document is unmodified after forking
assert OriginalUnchanged {
  all s, sPost: State, actor: AccountAddr, d, dv: Doc |
    NonOwnerFork[s, sPost, actor, d, dv]
    implies (d in sPost.D and sPost.pub[d] = s.pub[d]
             and sPost.val[d] = s.val[d])
}

-- D16d: The fork is the only addition to the document set
assert OnlyForkAdded {
  all s, sPost: State, actor: AccountAddr, d, dv: Doc |
    NonOwnerFork[s, sPost, actor, d, dv]
    implies sPost.D - s.D = dv
}

-- D16e: Unconstrained modify on a non-owner's published doc
-- violates the forking requirement (counterexample expected)
assert UnconstrainedRespectsForking {
  all s, sPost: State, actor: AccountAddr, d: Doc, c: Content |
    (UnconstrainedModify[s, sPost, actor, d, c] and
     d.account != actor and
     s.pub[d] in Published + Privashed)
    implies
    (some dv: sPost.D - s.D | dv.account = actor)
}

----------------------------------------------------------------------
-- Non-vacuity
----------------------------------------------------------------------

run FindFork {
  some s, sPost: State, actor: AccountAddr, d, dv: Doc |
    NonOwnerFork[s, sPost, actor, d, dv]
    and some s.val[d]
} for 5 but exactly 2 State

----------------------------------------------------------------------
-- Checks
----------------------------------------------------------------------

check ForkOwnership for 5 but exactly 2 State
check ForkChangesOwnership for 5 but exactly 2 State
check OriginalUnchanged for 5 but exactly 2 State
check OnlyForkAdded for 5 but exactly 2 State
check UnconstrainedRespectsForking for 5 but exactly 2 State
