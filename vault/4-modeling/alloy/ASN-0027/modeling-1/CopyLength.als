-- ASN-0027 / A4.length — CopyLength (POST, ensures)
-- Property: |Σ'.V(d_t)| = n_{d_t} + k
-- After copying k positions into document d_t, its length increases by k.

open util/integer

sig Addr {}

sig Doc {
  content: Int -> lone Addr,
  n: Int
} {
  n >= 0
  n =< 5
  all i: Int | (i >= 1 and i =< n) iff some content[i]
}

-- Overflow guard: keep arithmetic within 6-bit Int range
pred bounded[ps: Int, k: Int, pt: Int] {
  ps >= 0 and ps =< 10
  k >= 0 and k =< 10
  pt >= 0 and pt =< 10
}

-- Copy: insert k positions from source doc into target doc at position pt.
-- Source positions [ps, ps+k) are inserted at pt in the target.
-- Existing target positions at pt and beyond shift right by k.
pred Copy[ds, dt, dtPost: Doc, ps: Int, k: Int, pt: Int] {
  -- preconditions
  k >= 1
  ps >= 1
  plus[ps, minus[k, 1]] =< ds.n
  pt >= 1
  pt =< plus[dt.n, 1]

  -- positions before the insertion point: unchanged
  all i: Int | (i >= 1 and i < pt) implies
    dtPost.content[i] = dt.content[i]

  -- inserted positions: copied from source
  all j: Int | (j >= 0 and j < k) implies
    dtPost.content[plus[pt, j]] = ds.content[plus[ps, j]]

  -- positions at and after pt shift right by k
  all i: Int | (i >= pt and i =< dt.n) implies
    dtPost.content[plus[i, k]] = dt.content[i]

  -- nothing outside the new range
  all i: Int | (i < 1 or i > plus[dt.n, k]) implies
    no dtPost.content[i]
}

-- Property: resulting target length equals n_{d_t} + k
assert CopyLength {
  all ds, dt, dtPost: Doc, ps, k, pt: Int |
    (bounded[ps, k, pt] and Copy[ds, dt, dtPost, ps, k, pt]) implies
      dtPost.n = plus[dt.n, k]
}

check CopyLength for 5 but exactly 3 Doc, 6 Int

-- Non-vacuity: find a valid Copy with nontrivial documents
run FindCopy {
  some ds, dt, dtPost: Doc, ps, k, pt: Int |
    bounded[ps, k, pt] and Copy[ds, dt, dtPost, ps, k, pt] and dt.n > 0
} for 5 but exactly 3 Doc, 6 Int
