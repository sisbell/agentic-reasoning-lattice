-- P1-ContentImmutability
-- (A a : a in Sigma.A : Sigma'.iota(a) = Sigma.iota(a))
-- Content at allocated addresses never changes across transitions.

sig IAddr {}
sig Value {}

sig State {
  iota: IAddr -> lone Value   -- partial function IAddr -> Value
}

-- Allocated addresses = dom(iota)
fun allocated[s: State]: set IAddr {
  s.iota.Value
}

-- The two-state invariant: every pre-allocated address keeps its content
pred ContentImmutability[s, s2: State] {
  all a: allocated[s] | s2.iota[a] = s.iota[a]
}

-- Consequence: pre-allocated addresses remain allocated in post-state
-- (preserving content implies preserving membership in dom)
assert AllocatedPersists {
  all s, s2: State |
    ContentImmutability[s, s2] implies allocated[s] in allocated[s2]
}

-- Consequence: content immutability is reflexive
assert ImmutabilityReflexive {
  all s: State | ContentImmutability[s, s]
}

-- Non-vacuity: transition with existing content preserved and new addresses added
run NonVacuity {
  some s, s2: State |
    ContentImmutability[s, s2]
    and some allocated[s]
    and some allocated[s2] - allocated[s]
} for 5 but exactly 2 State

check AllocatedPersists for 5 but exactly 2 State
check ImmutabilityReflexive for 5 but exactly 1 State
