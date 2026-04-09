-- A4.pre — CopyPre: precondition for the Copy operation
--
-- d_s in Sigma.D /\ d_t in Sigma.D /\ k >= 1
-- /\ 1 =< p_s /\ p_s + k - 1 =< n_{d_s}
-- /\ 1 =< p_t =< n_{d_t} + 1

sig Doc {}

sig State {
  docs: set Doc,
  len: Doc -> lone Int
}

pred wellFormed[s: State] {
  -- len defined exactly for docs in state
  all d: Doc | (some s.len[d]) iff (d in s.docs)
  -- lengths are non-negative (bounded to avoid Int overflow)
  all d: s.docs | s.len[d] >= 0 and s.len[d] =< 10
}

-- Faithful encoding of the Copy precondition
pred CopyPre[s: State, ds: Doc, dt: Doc, ps: Int, k: Int, pt: Int] {
  ds in s.docs
  dt in s.docs
  k >= 1
  ps >= 1
  plus[ps, minus[k, 1]] =< s.len[ds]
  pt >= 1
  pt =< plus[s.len[dt], 1]
}

-- Overflow guard: keeps intermediate arithmetic within 6-bit Int range
pred bounded[ps: Int, k: Int, pt: Int] {
  ps >= 0 and ps =< 10
  k >= 0 and k =< 10
  pt >= 0 and pt =< 10
}

-- Derived: the last source position (ps + k - 1) is >= 1
assert SourceEndPositive {
  all s: State, ds, dt: Doc, ps, k, pt: Int |
    (wellFormed[s] and bounded[ps, k, pt] and CopyPre[s, ds, dt, ps, k, pt])
    implies plus[ps, minus[k, 1]] >= 1
}

-- Derived: source document has at least one position
assert SourceDocNonEmpty {
  all s: State, ds, dt: Doc, ps, k, pt: Int |
    (wellFormed[s] and bounded[ps, k, pt] and CopyPre[s, ds, dt, ps, k, pt])
    implies s.len[ds] >= 1
}

-- k = 0 is rejected by the precondition
assert RejectsZeroK {
  all s: State, ds, dt: Doc, ps, pt: Int |
    wellFormed[s] implies not CopyPre[s, ds, dt, ps, 0, pt]
}

-- Non-vacuity: the precondition is satisfiable
run FindCopyPre {
  some s: State, ds, dt: Doc, ps, k, pt: Int |
    wellFormed[s] and CopyPre[s, ds, dt, ps, k, pt]
} for 4 but exactly 1 State, 6 Int

check SourceEndPositive for 5 but exactly 1 State, 6 Int
check SourceDocNonEmpty for 5 but exactly 1 State, 6 Int
check RejectsZeroK for 5 but exactly 1 State, 6 Int
