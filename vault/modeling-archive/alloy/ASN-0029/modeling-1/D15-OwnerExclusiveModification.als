-- D15-OwnerExclusiveModification.als
-- ASN-0029 D15: Owner-Exclusive Modification
--
-- [op modifies Σ.V(d) ⟹ account(d) = actor(op)]
--
-- Design requirement on correct participants. The unconstrained
-- operation allows any actor; a counterexample demonstrates that
-- the ownership check is independently necessary.

sig Account {}

sig Doc {
  owner: one Account
}

sig Content {}

sig State {
  docs: set Doc,
  val: Doc -> lone Content
}

fact WellFormed {
  all s: State | (s.val).Content in s.docs
}

----------------------------------------------------------------------
-- Unconstrained modification (any account may act)
----------------------------------------------------------------------

pred Modify[s, s2: State, actor: Account, d: Doc, c: Content] {
  d in s.docs
  not (s.val[d] = c)
  s2.val[d] = c
  all d2: s.docs - d | s2.val[d2] = s.val[d2]
  s2.docs = s.docs
}

----------------------------------------------------------------------
-- D15 assertion (counterexample expected)
----------------------------------------------------------------------

-- Any content modification must be performed by the document's owner.
assert D15_OwnerExclusiveModification {
  all s, s2: State, actor: Account, d: Doc, c: Content |
    Modify[s, s2, actor, d, c] implies actor = d.owner
}

----------------------------------------------------------------------
-- Derived: enforcement makes two modifiers identical
----------------------------------------------------------------------

-- When D15 is enforced, any two successive modifications to the
-- same document are necessarily by the same account.
assert EnforcedNoSplitModifier {
  all s1, s2, s3: State, a1, a2: Account, d: Doc, c1, c2: Content |
    (a1 = d.owner and Modify[s1, s2, a1, d, c1] and
     a2 = d.owner and Modify[s2, s3, a2, d, c2])
    implies a1 = a2
}

----------------------------------------------------------------------
-- Checks
----------------------------------------------------------------------

check D15_OwnerExclusiveModification for 5 but exactly 2 State
check EnforcedNoSplitModifier for 5 but exactly 3 State

----------------------------------------------------------------------
-- Non-vacuity
----------------------------------------------------------------------

run NonVacuity {
  some s, s2: State, d: Doc, c: Content |
    Modify[s, s2, d.owner, d, c]
} for 4 but exactly 2 State
