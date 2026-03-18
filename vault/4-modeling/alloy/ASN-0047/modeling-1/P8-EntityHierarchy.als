-- P8-EntityHierarchy.als
-- Property: for every non-node entity, its parent is in the entity set.
-- (A e in E : not IsNode(e) : parent(e) in E)
-- Proved by induction: base (initial state vacuous), step (K.d requires parent in E, P1 preserves).

sig Tumbler {
  zeros: Int,
  parent: lone Tumbler
}

fact ZerosNonNeg {
  all t: Tumbler | t.zeros >= 0
}

-- Level predicates
pred IsNode[t: Tumbler]     { t.zeros = 0 }
pred IsAccount[t: Tumbler]  { t.zeros = 1 }
pred IsDocument[t: Tumbler] { t.zeros = 2 }

-- Parent well-formedness: defined exactly for non-nodes,
-- truncating drops one zero level.
fact ParentWellFormed {
  all t: Tumbler | {
    IsNode[t] implies no t.parent
    IsAccount[t] implies (one t.parent and IsNode[t.parent])
    IsDocument[t] implies (one t.parent and IsAccount[t.parent])
  }
}

sig State {
  E: set Tumbler
}

pred EntitySetValid[s: State] {
  all e: s.E | e.zeros =< 2
}

-- Initial state: single node, no other entities
pred IsInitialState[s: State] {
  one s.E
  all e: s.E | IsNode[e]
}

-- K.d: create a new entity; non-root requires parent in E
pred CreateEntity[s, s2: State, e: Tumbler] {
  e not in s.E
  e.zeros =< 2
  (not IsNode[e]) implies e.parent in s.E
  s2.E = s.E + e
}

-- Non-entity step: E unchanged
pred NonEntityStep[s, s2: State] {
  s2.E = s.E
}

pred ValidStep[s, s2: State] {
  (some e: Tumbler | CreateEntity[s, s2, e])
  or NonEntityStep[s, s2]
}

-- The property under test
pred EntityHierarchy[s: State] {
  all e: s.E | (not IsNode[e]) implies e.parent in s.E
}

-- P8 base: initial state satisfies hierarchy
assert P8_Base {
  all s: State | IsInitialState[s] implies EntityHierarchy[s]
}

-- P8 inductive: valid step preserves hierarchy
assert P8_Inductive {
  all s, s2: State |
    (EntitySetValid[s] and EntityHierarchy[s] and ValidStep[s, s2])
      implies EntityHierarchy[s2]
}

-- Non-vacuity: three-level state satisfying hierarchy
run NonVacuity {
  some s: State |
    EntityHierarchy[s]
    and (some e: s.E | IsNode[e])
    and (some e: s.E | IsAccount[e])
    and (some e: s.E | IsDocument[e])
} for 5 but exactly 1 State, 4 Int

check P8_Base for 5 but exactly 1 State, 4 Int
check P8_Inductive for 5 but exactly 2 State, 4 Int
