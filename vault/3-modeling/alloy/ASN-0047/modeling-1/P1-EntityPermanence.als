-- P1-EntityPermanence.als
-- Property: entities are permanent — once allocated, an entity is never
-- removed from the entity set in any subsequent state.
-- (A Σ → Σ' :: E ⊆ E')

-- Tumbler addresses with a zero-separator count determining level.
sig Tumbler {
  zeros: Int
}

fact ZerosNonNeg {
  all t: Tumbler | t.zeros >= 0
}

-- Level predicates
pred IsNode[t: Tumbler]     { t.zeros = 0 }
pred IsAccount[t: Tumbler]  { t.zeros = 1 }
pred IsDocument[t: Tumbler] { t.zeros = 2 }

-- State holding the entity set
sig State {
  E: set Tumbler
}

-- Entity set validity: only non-element tumblers (zeros <= 2)
pred EntitySetValid[s: State] {
  all e: s.E | e.zeros =< 2
}

-- Strata functions
fun E_node[s: State]: set Tumbler {
  { e: s.E | IsNode[e] }
}

fun E_account[s: State]: set Tumbler {
  { e: s.E | IsAccount[e] }
}

fun E_doc[s: State]: set Tumbler {
  { e: s.E | IsDocument[e] }
}

-- The entity-permanence predicate (two-state invariant)
pred EntityPermanence[s, s2: State] {
  s.E in s2.E
}

-- Elementary transition: create a new entity
pred CreateEntity[s, s2: State, e: Tumbler] {
  -- precondition: entity not yet allocated, valid entity address
  e not in s.E
  e.zeros =< 2
  -- postcondition: entity is added
  s2.E = s.E + e
}

-- Elementary transition: non-entity operation (content change, etc.)
pred NonEntityStep[s, s2: State] {
  s2.E = s.E
}

-- A valid elementary transition either creates an entity or leaves E unchanged.
-- No transition kind removes entities.
pred ValidStep[s, s2: State] {
  (some e: Tumbler | CreateEntity[s, s2, e])
  or NonEntityStep[s, s2]
}

-- P1: every valid step preserves entity permanence
assert P1_EntityPermanence {
  all s, s2: State |
    ValidStep[s, s2] implies EntityPermanence[s, s2]
}

-- P1a: node permanence
assert P1a_NodePermanence {
  all s, s2: State |
    ValidStep[s, s2] implies E_node[s] in E_node[s2]
}

-- P1b: account permanence
assert P1b_AccountPermanence {
  all s, s2: State |
    ValidStep[s, s2] implies E_account[s] in E_account[s2]
}

-- P1c: document permanence
assert P1c_DocumentPermanence {
  all s, s2: State |
    ValidStep[s, s2] implies E_doc[s] in E_doc[s2]
}

-- Non-vacuity: find a CreateEntity step where pre-state already has entities
run NonVacuity {
  some s, s2: State, e: Tumbler |
    EntitySetValid[s] and some s.E and CreateEntity[s, s2, e]
} for 5 but exactly 2 State, 4 Int

check P1_EntityPermanence for 5 but exactly 2 State, 4 Int
check P1a_NodePermanence for 5 but exactly 2 State, 4 Int
check P1b_AccountPermanence for 5 but exactly 2 State, 4 Int
check P1c_DocumentPermanence for 5 but exactly 2 State, 4 Int
