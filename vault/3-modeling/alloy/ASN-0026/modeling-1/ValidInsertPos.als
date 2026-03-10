-- P9 (pre) — ValidInsertPos
-- Precondition for Insert: 1 <= p <= n_d + 1  and  k >= 1
--
-- n_d is the current length of document d.
-- p is the target insertion position (1-based).
-- k is the number of bytes to insert (must be at least 1).

sig DocId {}

sig State {
  docs: set DocId,
  docLen: DocId -> lone Int
}

-- Well-formedness: docLen defined exactly for docs, lengths non-negative,
-- and nd+1 does not overflow (so plus[nd,1] > nd >= 0).
pred wfState[s: State] {
  s.docLen.Int = s.docs
  all d: s.docs | s.docLen[d] >= 0
  all d: s.docs | plus[s.docLen[d], 1] > s.docLen[d]
}

-- Insert precondition: position p is valid for document d with k bytes to insert.
pred ValidInsertPos[s: State, d: DocId, p: Int, k: Int] {
  d in s.docs
  p >= 1
  p =< plus[s.docLen[d], 1]
  k >= 1
}

-- P9-LB: ValidInsertPos implies p >= 1
assert P9_LowerBound {
  all s: State, d: DocId, p, k: Int |
    ValidInsertPos[s, d, p, k] implies p >= 1
}

-- P9-UB: ValidInsertPos implies p <= n_d + 1
assert P9_UpperBound {
  all s: State, d: DocId, p, k: Int |
    ValidInsertPos[s, d, p, k] implies p =< plus[s.docLen[d], 1]
}

-- P9-K: ValidInsertPos implies k >= 1
assert P9_KBound {
  all s: State, d: DocId, p, k: Int |
    ValidInsertPos[s, d, p, k] implies k >= 1
}

-- P9-Start: position 1 is always valid for an existing document
assert P9_BoundaryStart {
  all s: State, d: DocId, k: Int |
    (wfState[s] and d in s.docs and k >= 1) implies ValidInsertPos[s, d, 1, k]
}

-- P9-End: position n_d + 1 is always valid for an existing document
assert P9_BoundaryEnd {
  all s: State, d: DocId, k: Int |
    (wfState[s] and d in s.docs and k >= 1) implies
      ValidInsertPos[s, d, plus[s.docLen[d], 1], k]
}

-- Non-vacuity: a valid insert configuration exists
run NonVacuous {
  some s: State, d: DocId, p, k: Int |
    wfState[s] and ValidInsertPos[s, d, p, k]
} for 3 but 5 Int

check P9_LowerBound    for 4 but 5 Int
check P9_UpperBound    for 4 but 5 Int
check P9_KBound        for 4 but 5 Int
check P9_BoundaryStart for 4 but 5 Int
check P9_BoundaryEnd   for 4 but 5 Int
