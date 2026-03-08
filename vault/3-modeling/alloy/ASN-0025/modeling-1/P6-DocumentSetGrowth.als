-- P6 — DocumentSetGrowth (INV, predicate(State, State))
-- Property: Σ.D ⊆ Σ'.D
-- Document set only grows across transitions.

sig IAddr {}
sig Value {}

sig State {
  iota: IAddr -> lone Value,        -- Σ.ι : IAddr ⇸ Value
  docs: set IAddr                   -- Σ.D ⊆ Σ.A
}

-- Σ.A = dom(Σ.ι)
fun allocated[s: State]: set IAddr {
  s.iota.Value
}

-- Well-formedness: D ⊆ A
pred wellFormed[s: State] {
  s.docs in allocated[s]
}

-- P6: document set only grows
pred DocumentSetGrowth[s, s2: State] {
  s.docs in s2.docs
}

-- Consequence: under P6 + well-formedness of post-state,
-- every pre-existing document remains allocated in post-state
assert DocsRemainAllocated {
  all s, s2: State |
    (wellFormed[s2] and DocumentSetGrowth[s, s2]) implies
      s.docs in allocated[s2]
}

-- Consequence: DocumentSetGrowth is reflexive
assert GrowthReflexive {
  all s: State | DocumentSetGrowth[s, s]
}

-- Non-vacuity: transition with non-empty D that grows
run NonVacuity {
  some s, s2: State |
    wellFormed[s] and wellFormed[s2]
    and DocumentSetGrowth[s, s2]
    and some s.docs
    and some s2.docs - s.docs
} for 5 but exactly 2 State

check DocsRemainAllocated for 5 but exactly 2 State
check GrowthReflexive for 5 but exactly 1 State
