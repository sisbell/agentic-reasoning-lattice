-- A9 — ReachabilityDecay (LEMMA, lemma)
-- Property: If reachable(a, Σ), then there exists a finite sequence of
-- operations producing Σ' with ¬reachable(a, Σ').
--
-- Strategy: model a trace where each step removes one reference to a
-- target address via delete.  The trace forces progress: while any
-- document still references Target, the next step removes one such
-- reference.  After at most |Doc| steps, Target is unreachable.

open util/ordering[State]

sig Addr {}
one sig Target extends Addr {}
sig Doc {}

sig State {
  contents: Doc -> set Addr
}

-- refs(a, s): documents that reference address a in state s
fun refs[a: Addr, s: State]: set Doc {
  { d: Doc | a in s.contents[d] }
}

-- reachable(a, s) iff refs(a, s) non-empty
pred reachable[a: Addr, s: State] {
  some refs[a, s]
}

-- Trace: each step removes one (doc, Target) pair from contents,
-- or idles when no document references Target.
fact trace {
  all s: State - last |
    let sPost = s.next |
      -- progress: remove one reference to Target
      (some d: Doc |
        d -> Target in s.contents and
        sPost.contents = s.contents - (d -> Target))
      or
      -- idle: Target already unreachable, state unchanged
      (Target not in Doc.(s.contents) and
        sPost.contents = s.contents)
}

-- A9: if Target is reachable in the initial state,
-- it is unreachable by the final state
assert ReachabilityDecay {
  reachable[Target, first] implies not reachable[Target, last]
}

-- Scope: 4 docs need at most 4 removal steps = 5 states
check ReachabilityDecay for 4 but exactly 5 State

-- Non-vacuity: find a trace where Target starts reachable and ends unreachable
run NonVacuity {
  reachable[Target, first] and not reachable[Target, last]
} for 4 but exactly 5 State
