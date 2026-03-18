-- EntityCreatable.als
-- K.d precondition: when creating a non-node entity, parent(e) must be in E.
-- Root nodes (IsNode(e)) have no parent requirement.

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

-- Parent well-formedness: nodes have no parent, accounts have node parent,
-- documents have account parent.
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

-- The precondition under test
pred EntityCreatable[s: State, e: Tumbler] {
  e not in s.E
  e.zeros =< 2
  (not IsNode[e]) implies e.parent in s.E
}

-- K.d: entity creation guarded by EntityCreatable
pred CreateEntity[s, s2: State, e: Tumbler] {
  EntityCreatable[s, e]
  s2.E = s.E + e
}

-- Property 1: Creating a node never requires a parent check
-- (the parent clause is vacuously true for nodes)
assert NodeCreationUnguarded {
  all s: State, e: Tumbler |
    (EntitySetValid[s] and IsNode[e] and e not in s.E)
      implies EntityCreatable[s, e]
}

-- Property 2: Creating an account requires its node parent in E
assert AccountNeedsParent {
  all s: State, e: Tumbler |
    (EntitySetValid[s] and IsAccount[e] and e not in s.E
     and e.parent not in s.E)
      implies not EntityCreatable[s, e]
}

-- Property 3: Creating a document requires its account parent in E
assert DocumentNeedsParent {
  all s: State, e: Tumbler |
    (EntitySetValid[s] and IsDocument[e] and e not in s.E
     and e.parent not in s.E)
      implies not EntityCreatable[s, e]
}

-- Property 4: CreateEntity preserves EntitySetValid
assert CreatePreservesValid {
  all s, s2: State, e: Tumbler |
    (EntitySetValid[s] and CreateEntity[s, s2, e])
      implies EntitySetValid[s2]
}

-- Non-vacuity: find a state where we can create an account
-- (requires its node parent already in E)
run FindAccountCreation {
  some s, s2: State, e: Tumbler |
    EntitySetValid[s]
    and IsAccount[e]
    and CreateEntity[s, s2, e]
} for 5 but exactly 2 State, 4 Int

check NodeCreationUnguarded for 5 but exactly 1 State, 4 Int
check AccountNeedsParent for 5 but exactly 1 State, 4 Int
check DocumentNeedsParent for 5 but exactly 1 State, 4 Int
check CreatePreservesValid for 5 but exactly 2 State, 4 Int
