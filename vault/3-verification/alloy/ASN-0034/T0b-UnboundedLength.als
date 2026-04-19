-- ASN-0034 Property T0(b): UnboundedLength
-- (A n in N : n >= 1 : (E t in T :: #t >= n))
-- T is the set of all finite sequences over N with length >= 1.
-- For any n, the constant sequence [1,1,...,1] of length n witnesses the claim.

sig Tumbler {
  len: Int   -- #t: length of the tumbler (number of components)
}

-- Axiom: T is the set of all finite sequences over N with length >= 1.
-- In bounded scope this means: every tumbler has length >= 1, and for
-- every representable positive integer n, some tumbler has length n.
fact TumblerAxiom {
  all t: Tumbler | t.len >= 1
  all n: Int | n >= 1 implies some t: Tumbler | t.len = n
}

-- T0(b): for every n >= 1, there exists a tumbler with #t >= n
assert UnboundedLength {
  all n: Int | n >= 1 implies some t: Tumbler | t.len >= n
}

-- Non-vacuity: the axiom is satisfiable and tumblers exist
run NonVacuity {
  some t: Tumbler | t.len >= 1
} for 8 but 4 Int

check UnboundedLength for 8 but 4 Int
