-- A10 — PublicationObligation (INV, predicate(Addr, State))
-- For content that has been published: reachable(a, S) is maintained
-- across all states.
--
-- Contractual, not architectural.  The architecture permits DELETE on
-- any V-space position without checking publication status.
-- We therefore expect a counterexample: deleting the sole reference
-- to a published address makes it unreachable.

sig Addr {}
sig Slot {}
sig Doc {}

sig State {
  docs: set Doc,
  val: Doc -> Slot -> lone Addr
} {
  -- val only defined for docs in this state
  all d: Doc | d not in docs implies no val[d]
}

-- refs(a, s): (doc, slot) pairs that reference address a
fun refs[a: Addr, s: State]: Doc -> Slot {
  { d: s.docs, p: Slot | s.val[d][p] = a }
}

-- reachable(a, s): a is referenced by some document in s
pred reachable[a: Addr, s: State] {
  some refs[a, s]
}

-- Delete: remove the mapping at slot p in document d.
-- No publication-status check — any occupied slot may be deleted.
pred Delete[s, sPost: State, d: Doc, p: Slot] {
  -- precondition: d is in the state, slot is occupied
  d in s.docs
  some s.val[d][p]

  -- effect: remove the mapping at (d, p)
  sPost.val = s.val - (d -> p -> Addr)

  -- frame: document set unchanged
  sPost.docs = s.docs
}

-- A10: if a is reachable before a Delete, it remains reachable after
assert PublicationObligation {
  all s, sPost: State, d: Doc, p: Slot, a: Addr |
    (reachable[a, s] and Delete[s, sPost, d, p])
      implies reachable[a, sPost]
}

check PublicationObligation for 5 but exactly 2 State

-- Non-vacuity: a delete that touches a reachable address
run NonVacuity {
  some s, sPost: State, d: Doc, p: Slot, a: Addr |
    reachable[a, s] and Delete[s, sPost, d, p] and s.val[d][p] = a
} for 4 but exactly 2 State
