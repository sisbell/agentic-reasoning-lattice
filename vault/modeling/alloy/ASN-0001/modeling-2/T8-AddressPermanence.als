open util/ordering[State]

sig Addr {}
sig Content {}

sig State {
  assigned: Addr -> lone Content
}

-- Operation: assign content to an unassigned address
pred Assign[s, s2: State, a: Addr, c: Content] {
  -- precondition: address not yet assigned
  no s.assigned[a]
  -- postcondition: address now maps to content
  s2.assigned[a] = c
  -- frame: all other assignments unchanged
  all a2: Addr - a | s2.assigned[a2] = s.assigned[a2]
}

-- Operation: no change
pred Skip[s, s2: State] {
  s2.assigned = s.assigned
}

-- System trace: each transition is either Assign or Skip
fact Trace {
  all s: State - last |
    let s2 = s.next |
      Skip[s, s2] or (some a: Addr, c: Content | Assign[s, s2, a, c])
}

-- T8: Address Permanence
-- Once a maps to c, it stays that way in all subsequent states
assert AddressPermanence {
  all s1, s2: State, a: Addr, c: Content |
    (a -> c in s1.assigned and gte[s2, s1])
      implies a -> c in s2.assigned
}

-- Also check the contrapositive angle: no operation changes an existing mapping
assert NoReassignment {
  all s: State - last, a: Addr |
    let s2 = s.next |
      some s.assigned[a] implies s2.assigned[a] = s.assigned[a]
}

-- Non-vacuity: find a trace where an assignment actually happens
run NonVacuity {
  some s1, s2: State, a: Addr, c: Content |
    no s1.assigned[a] and
    a -> c in s2.assigned and
    lt[s1, s2]
} for 4 but exactly 3 State

check AddressPermanence for 5 but exactly 4 State
check NoReassignment for 5 but exactly 4 State
