-- P0 — ISpaceGrowth (INV, predicate(State, State))
-- Property: Σ.A ⊆ Σ'.A
-- Allocated addresses only grow across transitions.

sig IAddr {}
sig Value {}

sig State {
  iota: IAddr -> lone Value        -- Σ.ι : IAddr ⇸ Value
}

-- Σ.A = dom(Σ.ι)
fun allocated[s: State]: set IAddr {
  s.iota.Value
}

-- P0: allocated addresses only grow
pred ISpaceGrowth[s, s2: State] {
  allocated[s] in allocated[s2]
}

-- Assert P0 for all state pairs
assert P0_ISpaceGrowth {
  all s, s2: State |
    ISpaceGrowth[s, s2]
}

-- Non-vacuity: a transition satisfying P0 with nonempty allocation exists
run NonVacuity {
  some s, s2: State |
    s != s2 and ISpaceGrowth[s, s2] and some allocated[s]
} for 4 but exactly 2 State

check P0_ISpaceGrowth for 5 but exactly 2 State
