-- D5-OwnershipRights.als
-- ASN-0029 D5: Ownership Rights
--
-- For document d with owner account(d):
--   (a) only the owner may alter Σ.V(d)
--   (b) only the owner may create or remove links stored in d
--   (c) only owner and designated associates may access d when private
--   (d) only the owner may allocate new tumblers extending d's prefix
--
-- Design requirement on correct participants. Operations are
-- unconstrained (any actor may act); counterexamples demonstrate
-- each ownership right is independently necessary.

sig Account {}

sig Doc {
  owner: one Account
}

sig Content {}

sig State {
  docs: set Doc,
  val: Doc -> lone Content,
  links: Doc -> set Doc,
  priv: set Doc,
  assoc: Doc -> set Account
}

fact WellFormed {
  all s: State {
    (s.val).Content in s.docs
    (s.links).Doc in s.docs
    s.priv in s.docs
    (s.assoc).Account in s.docs
  }
}

----------------------------------------------------------------------
-- Unconstrained operations (any account may act)
----------------------------------------------------------------------

-- (a) Actor modifies content of document d
pred ModifyContent[s, s2: State, actor: Account, d: Doc, c: Content] {
  d in s.docs
  not (s.val[d] = c)
  s2.val[d] = c
  all d2: s.docs - d | s2.val[d2] = s.val[d2]
  s2.docs = s.docs
  s2.links = s.links
  s2.priv = s.priv
  s2.assoc = s.assoc
}

-- (b) Actor modifies links stored in document d
pred ModifyLinks[s, s2: State, actor: Account, d: Doc] {
  d in s.docs
  not (s2.links[d] = s.links[d])
  all d2: s.docs - d | s2.links[d2] = s.links[d2]
  s2.docs = s.docs
  s2.val = s.val
  s2.priv = s.priv
  s2.assoc = s.assoc
}

-- (d) Actor allocates a new document under the same owner as d
pred AllocateDoc[s, s2: State, actor: Account, d: Doc, sub: Doc] {
  d in s.docs
  sub not in s.docs
  sub.owner = d.owner
  s2.docs = s.docs + sub
  all d2: s.docs | s2.val[d2] = s.val[d2]
  all d2: s.docs | s2.links[d2] = s.links[d2]
  s2.priv = s.priv
  s2.assoc = s.assoc
}

----------------------------------------------------------------------
-- D5 assertions (counterexamples expected for a, b, c, d)
----------------------------------------------------------------------

-- D5(a): content modification requires ownership
assert D5a_ContentRequiresOwner {
  all s, s2: State, actor: Account, d: Doc, c: Content |
    ModifyContent[s, s2, actor, d, c] implies actor = d.owner
}

-- D5(b): link modification requires ownership
assert D5b_LinksRequireOwner {
  all s, s2: State, actor: Account, d: Doc |
    ModifyLinks[s, s2, actor, d] implies actor = d.owner
}

-- D5(c): private document access requires owner or associate
assert D5c_PrivateAccessRestricted {
  all s: State, actor: Account, d: Doc |
    d in s.priv implies (actor = d.owner or actor in s.assoc[d])
}

-- D5(d): allocation requires ownership
assert D5d_AllocationRequiresOwner {
  all s, s2: State, actor: Account, d: Doc, sub: Doc |
    AllocateDoc[s, s2, actor, d, sub] implies actor = d.owner
}

----------------------------------------------------------------------
-- Derived: under enforcement, no split ownership
----------------------------------------------------------------------

-- When D5 is enforced, any two content modifications to the same
-- document must be performed by the same account (both = d.owner).
assert NoSplitOwnership {
  all s1, s2, s3: State, a1, a2: Account, d: Doc, c1, c2: Content |
    (a1 = d.owner and ModifyContent[s1, s2, a1, d, c1] and
     a2 = d.owner and ModifyContent[s2, s3, a2, d, c2])
    implies a1 = a2
}

----------------------------------------------------------------------
-- Checks
----------------------------------------------------------------------

check D5a_ContentRequiresOwner for 5 but exactly 2 State
check D5b_LinksRequireOwner for 5 but exactly 2 State
check D5c_PrivateAccessRestricted for 5
check D5d_AllocationRequiresOwner for 5 but exactly 2 State
check NoSplitOwnership for 5 but exactly 3 State

----------------------------------------------------------------------
-- Non-vacuity
----------------------------------------------------------------------

run NonVacuity {
  some s, s2: State, d: Doc, c: Content |
    ModifyContent[s, s2, d.owner, d, c] and
    some s.priv and some s.assoc
} for 5 but exactly 2 State
