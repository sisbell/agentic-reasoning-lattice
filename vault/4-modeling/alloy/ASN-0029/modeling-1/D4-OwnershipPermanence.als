-- D4-OwnershipPermanence.als
-- Lemma D4: account(d) in Σ = account(d) in Σ' for all transitions.
-- Derived from D2 (DocumentPermanence) and D3 (StructuralOwnership).
--
-- D3 establishes that any state-level ownership assignment must agree
-- with the structural account() function. D2 establishes that documents
-- persist across transitions. D4 combines both: for any document that
-- exists in the pre-state, its owner is identical in the post-state.

----------------------------------------------------------------------
-- Address structure (from D3)
----------------------------------------------------------------------

sig Tumbler {
  zeros: Int,
  parent: lone Tumbler
}

fact TreeStructure {
  no t: Tumbler | t in t.^parent
  all t: Tumbler | t.zeros >= 0
  all t: Tumbler | t.zeros = 0 iff no t.parent
  all t: Tumbler | some t.parent implies
    t.parent.zeros = minus[t.zeros, 1]
}

fun AccountAddr: set Tumbler {
  { t: Tumbler | t.zeros = 1 }
}

fun DocAddr: set Tumbler {
  { t: Tumbler | t.zeros = 2 }
}

-- Structural account prefix: unique account ancestor of d
fun account[d: Tumbler]: set Tumbler {
  AccountAddr & d.*parent
}

----------------------------------------------------------------------
-- State (combines D2 and D3 elements)
----------------------------------------------------------------------

sig State {
  docs: set Tumbler,
  owner: Tumbler -> lone Tumbler
}

fact DocsAreDocAddrs {
  all s: State | s.docs in DocAddr
}

-- D3 premise: state-level owner agrees with structural account
fact StructuralOwnership {
  all s: State, d: s.docs |
    s.owner[d] = account[d]
}

----------------------------------------------------------------------
-- Transition (D2 premise)
----------------------------------------------------------------------

-- D2: documents, once created, are never removed
pred Step[s, sPost: State] {
  s.docs in sPost.docs
}

----------------------------------------------------------------------
-- D4: OwnershipPermanence
----------------------------------------------------------------------

-- For any document in the pre-state, its owner is the same
-- in both states. Follows because:
--   d in s.docs  and  Step[s,sPost]  =>  d in sPost.docs   (D2)
--   s.owner[d] = account[d]                                 (D3 on s)
--   sPost.owner[d] = account[d]                             (D3 on sPost)
--   therefore s.owner[d] = sPost.owner[d]

assert OwnershipPermanence {
  all s, sPost: State, d: Tumbler |
    (Step[s, sPost] and d in s.docs) implies
      s.owner[d] = sPost.owner[d]
}

check OwnershipPermanence for 5 but exactly 2 State, 4 Int

----------------------------------------------------------------------
-- Non-vacuity: a transition where a new document is created
----------------------------------------------------------------------

run NonVacuity {
  some s, sPost: State, d: Tumbler |
    Step[s, sPost] and d in s.docs and sPost.docs != s.docs
} for 5 but exactly 2 State, 4 Int
