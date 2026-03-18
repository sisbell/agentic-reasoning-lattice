-- T0(b): UnboundedLength
-- For every positive integer n, there exists a tumbler of length >= n.
-- The tumbler type imposes no upper bound on sequence length.

sig Tumbler {
  len: Int
} {
  len >= 1
}

-- The tumbler type admits sequences of every positive length.
-- Models that T contains all finite sequences of naturals: for any
-- positive length, a tumbler of that length is constructible.
fact TypeCompleteness {
  all n: Int | n >= 1 implies some t: Tumbler | t.len = n
}

-- T0(b): unbounded length property
assert UnboundedLength {
  all n: Int | n >= 1 implies some t: Tumbler | t.len >= n
}

check UnboundedLength for 8 but 4 Int

-- Non-vacuity: the model is satisfiable (type completeness is achievable)
run NonVacuity {} for 8 but 4 Int
