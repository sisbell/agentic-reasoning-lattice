-- T8 — AddressPermanence
-- Once a tumbler is assigned to content, that binding persists in all
-- subsequent states: no removal, no reassignment.

sig Tumbler {}
sig Content {}

sig State {
  assigned: Tumbler -> lone Content,
  next:     lone State
}

-- A single transition is valid iff every existing assignment is preserved.
-- Because assigned is a partial function (lone), subset inclusion implies
-- both non-removal and non-change: if t->c is in s.assigned, it must also
-- be in sPost.assigned; the lone multiplicity prevents t->c2 coexisting with
-- t->c in sPost.assigned, so the value cannot silently shift.
pred ValidStep[s, sPost: State] {
  s.assigned in sPost.assigned
}

-- The system is valid iff every taken transition is a ValidStep.
pred SystemValid {
  all s: State | some s.next implies ValidStep[s, s.next]
}

-- AddressPermanence: single-step validity implies multi-step validity.
-- If the system is valid and sPost is reachable from s (one or more steps),
-- then every assignment present in s is still present in sPost.
assert AddressPermanence {
  SystemValid implies
    all s, sPost: State |
      sPost in s.^next implies s.assigned in sPost.assigned
}

-- Violation witness for the negation of ValidStep: find a transition that
-- drops an assignment.  Should produce an instance (property is NOT vacuous
-- — violations are possible when SystemValid is not imposed).
assert NoDropWithoutConstraint {
  all s: State | some s.next implies s.assigned in s.next.assigned
}

-- Non-vacuity: confirm there exists a valid system where an assignment
-- is made in an early state and is still present two steps later.
run Witness {
  SystemValid
  some s, sPost: State |
    sPost in s.^next and
    some t: Tumbler, c: Content | t -> c in s.assigned and t -> c in sPost.assigned
} for 5 but exactly 3 State

check AddressPermanence       for 5 but exactly 3 State
check NoDropWithoutConstraint for 5 but exactly 2 State
