-- A0 — ReachabilityNonPermanent
-- Lemma: there exist transitions Σ → Σ' such that
--   reachable(a, Σ) ∧ ¬reachable(a, Σ').
--
-- Strategy: assert the negation (reachability is permanent),
-- expect a counterexample confirming the lemma.

sig Addr {}
sig Doc {}

sig State {
  -- each (doc, addr) pair in contents means doc references addr at some position
  contents: Doc -> set Addr
}

-- refs(a, s): documents that reference address a in state s
fun refs[a: Addr, s: State]: set Doc {
  { d: Doc | a in s.contents[d] }
}

-- reachable(a, s) ≡ refs(a, s) ≠ ∅
pred reachable[a: Addr, s: State] {
  some refs[a, s]
}

-- Negation of the lemma: if reachability were permanent, this would hold.
-- A counterexample witnesses the lemma.
assert ReachabilityPermanent {
  all a: Addr, s, sPost: State |
    reachable[a, s] implies reachable[a, sPost]
}

check ReachabilityPermanent for 4 but exactly 2 State

-- Non-vacuity: find states witnessing the lemma directly
run Witness {
  some a: Addr, s, sPost: State |
    reachable[a, s] and not reachable[a, sPost]
} for 4 but exactly 2 State
