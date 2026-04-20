-- Reference Alloy model: demonstrates idiomatic patterns
-- (sig, pred, fun, assert, check, run)

-- Domain types
sig Key {}
sig Value {}

-- State with relations
sig State {
  store: Key -> lone Value,   -- partial function
  active: set Key             -- set-valued field
}

-- State invariant
pred wellFormed[s: State] {
  -- every key with a value is active
  all k: Key | some s.store[k] implies k in s.active
}

-- Operation: two-state predicate with pre/post
pred Add[s, sPost: State, k: Key, v: Value] {
  -- precondition: key is not already active
  k not in s.active

  -- postcondition: key maps to value
  sPost.store[k] = v
  k in sPost.active

  -- frame: everything else unchanged
  all k2: Key - k | sPost.store[k2] = s.store[k2]
  sPost.active = s.active + k
}

-- Derived claim: count of active keys
fun activeCount[s: State]: Int {
  #s.active
}

-- Claim: Add preserves well-formedness
assert AddPreservesWF {
  all s, sPost: State, k: Key, v: Value |
    (wellFormed[s] and Add[s, sPost, k, v]) implies wellFormed[sPost]
}

-- Claim: Add does not remove existing keys
assert AddMonotonic {
  all s, sPost: State, k: Key, v: Value |
    (Add[s, sPost, k, v]) implies s.active in sPost.active
}

-- Non-vacuity: can we find a valid Add?
run FindAdd {
  some s, sPost: State, k: Key, v: Value |
    wellFormed[s] and Add[s, sPost, k, v]
} for 4 but exactly 2 State

check AddPreservesWF for 5 but exactly 2 State
check AddMonotonic for 5 but exactly 2 State
