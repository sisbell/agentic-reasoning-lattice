-- P1 — ISpaceMonotone
-- I-space addresses are never deallocated across transitions.
-- For any transition Sigma -> Sigma':
--   a in dom(Sigma.I)  ==>  a in dom(Sigma'.I)

sig Addr {}
sig Byte {}

sig State {
  ispace: Addr -> lone Byte       -- partial function Addr -> Byte
}

-- Domain of I-space: the set of allocated addresses
fun allocated[s: State]: set Addr {
  s.ispace.Byte
}

-- P1: I-space monotonicity predicate
pred ISpaceMonotone[s, s2: State] {
  all a: Addr | a in allocated[s] implies a in allocated[s2]
}

-- The quantified form is equivalent to subset inclusion
assert MonotoneIsSubset {
  all s, s2: State |
    ISpaceMonotone[s, s2] iff allocated[s] in allocated[s2]
}

-- Monotonicity composes: if s->s2 and s2->s3 are both
-- monotone then s->s3 is monotone
assert MonotoneTransitive {
  all s1, s2, s3: State |
    (ISpaceMonotone[s1, s2] and ISpaceMonotone[s2, s3])
      implies ISpaceMonotone[s1, s3]
}

-- Domain size never decreases under a monotone transition
assert MonotoneSizeNonDecreasing {
  all s, s2: State |
    ISpaceMonotone[s, s2] implies #allocated[s] =< #allocated[s2]
}

-- Non-vacuity: a monotone transition exists where the domain
-- actually grows (new address allocated, none removed)
run NonVacuity {
  some s, s2: State |
    ISpaceMonotone[s, s2]
    and some allocated[s]
    and some (allocated[s2] - allocated[s])
} for 4 but exactly 2 State

check MonotoneIsSubset for 5 but exactly 2 State
check MonotoneTransitive for 5 but exactly 3 State
check MonotoneSizeNonDecreasing for 5 but exactly 2 State, 5 Int
