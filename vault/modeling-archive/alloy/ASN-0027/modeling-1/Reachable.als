-- Reachable property
-- reachable(a, S) iff refs(a) != empty
-- refs(a) = {(d, p) : d in S.docs, V(d)(p) = a}

sig Addr {}

-- Slot abstracts position indices within a document
sig Slot {}

sig Doc {
  val: Slot -> lone Addr
}

sig State {
  docs: set Doc
}

-- refs(a): all (doc, slot) pairs that reference address a
fun refs[a: Addr, s: State]: Doc -> Slot {
  { d: s.docs, p: Slot | d.val[p] = a }
}

-- reachable(a, s): a is referenced by some document in s
pred reachable[a: Addr, s: State] {
  some refs[a, s]
}

-- Definitional consistency: reachable iff refs non-empty
assert ReachableIffRefs {
  all s: State, a: Addr |
    reachable[a, s] iff some refs[a, s]
}

-- Empty document set implies nothing reachable
assert EmptyStateUnreachable {
  all s: State |
    no s.docs implies (no a: Addr | reachable[a, s])
}

-- Monotonicity: more docs can only increase reachability
assert DocsMonotone {
  all s1, s2: State |
    s1.docs in s2.docs implies
      (all a: Addr | reachable[a, s1] implies reachable[a, s2])
}

-- An address not in the range of any doc's val is unreachable
assert UnreferencedUnreachable {
  all s: State, a: Addr |
    (no d: s.docs, p: Slot | d.val[p] = a) implies not reachable[a, s]
}

-- Non-vacuity: state with both reachable and unreachable addresses
run FindMixed {
  some s: State {
    some a1: Addr | reachable[a1, s]
    some a2: Addr | not reachable[a2, s]
  }
} for 4 but exactly 1 State

check ReachableIffRefs for 5 but exactly 1 State
check EmptyStateUnreachable for 5 but exactly 1 State
check DocsMonotone for 5 but exactly 2 State
check UnreferencedUnreachable for 5 but exactly 1 State
