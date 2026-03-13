-- T8 — AllocationPermanence
-- Once a tumbler is allocated, it remains allocated in all subsequent states.
-- The set of allocated addresses is monotonically non-decreasing.

open util/ordering[State]

sig Tumbler {}

sig State {
  allocated: set Tumbler
}

-- Monotonicity: allocated sets grow along the trace
fact AllocationGrowsMonotonically {
  all s: State | some s.next implies s.allocated in s.next.allocated
}

-- T8: once allocated, always allocated in all future states (transitive closure form)
assert AllocationPermanence {
  all s1, s2: State, t: Tumbler |
    (t in s1.allocated and lt[s1, s2]) implies t in s2.allocated
}

-- T8 restated: no tumbler ever leaves the allocated set
assert NeverDeallocated {
  all s: State, t: Tumbler |
    t in s.allocated implies all s2: s.nexts | t in s2.allocated
}

-- Non-vacuity: find a trace where a new tumbler gets allocated
run NonVacuity {
  some t: Tumbler, s: State |
    some s.next and t not in s.allocated and t in s.next.allocated
} for 4 but exactly 3 State

check AllocationPermanence for 5 but exactly 4 State
check NeverDeallocated for 5 but exactly 4 State
