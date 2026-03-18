-- EntitySetValid: E contains only non-element entities (zeros <= 2)
-- and the level predicates partition E into exactly three strata.

-- Tumbler addresses with a zero-separator count determining level.
sig Tumbler {
  zeros: Int   -- number of zero separators
}

-- Constrain zeros to be non-negative
fact ZerosNonNeg {
  all t: Tumbler | t.zeros >= 0
}

-- Level predicates based on zero count
pred IsNode[t: Tumbler]     { t.zeros = 0 }
pred IsAccount[t: Tumbler]  { t.zeros = 1 }
pred IsDocument[t: Tumbler] { t.zeros = 2 }
pred IsElement[t: Tumbler]  { t.zeros >= 3 }

-- ValidAddress: any tumbler with non-negative zeros count
pred ValidAddress[t: Tumbler] {
  t.zeros >= 0
}

-- State holding the entity set
sig State {
  E: set Tumbler
}

-- The invariant under test: EntitySetValid
pred EntitySetValid[s: State] {
  -- E subset of valid addresses with zeros <= 2
  all e: s.E | ValidAddress[e] and e.zeros =< 2
  -- Equivalently: no element in E
  all e: s.E | not IsElement[e]
}

-- Derived strata
fun E_node[s: State]: set Tumbler {
  { e: s.E | IsNode[e] }
}

fun E_account[s: State]: set Tumbler {
  { e: s.E | IsAccount[e] }
}

fun E_doc[s: State]: set Tumbler {
  { e: s.E | IsDocument[e] }
}

-- Property 1: EntitySetValid implies the three strata partition E
assert StrataPartition {
  all s: State |
    EntitySetValid[s] implies
      (E_node[s] + E_account[s] + E_doc[s] = s.E
       and disj[E_node[s], E_account[s], E_doc[s]])
}

-- Property 2: EntitySetValid implies no element in E
assert NoElements {
  all s: State |
    EntitySetValid[s] implies
      (no e: s.E | IsElement[e])
}

-- Property 3: zeros <= 2 equivalent to not IsElement
assert ZeroBoundEquivNotElement {
  all t: Tumbler |
    (ValidAddress[t] and t.zeros =< 2) iff not IsElement[t]
}

-- Non-vacuity: find a state satisfying EntitySetValid with all three strata populated
run FindValid {
  some s: State |
    EntitySetValid[s]
    and some E_node[s]
    and some E_account[s]
    and some E_doc[s]
} for 5 but exactly 1 State, 4 Int

check StrataPartition for 5 but exactly 1 State, 4 Int
check NoElements for 5 but exactly 1 State, 4 Int
check ZeroBoundEquivNotElement for 5 but 4 Int
