-- ASN-0027 / A2.length — DeleteLength (POST, ensures)
-- Property: |Σ'.V(d)| = n_d − k
-- After deleting k positions from document d, the resulting length is n_d - k.

open util/integer

sig Addr {}

sig Doc {
  content: Int -> lone Addr,
  n: Int
} {
  n >= 0
  n =< 5
  all i: Int | (i >= 0 and i < n) iff some content[i]
}

-- Delete k contiguous positions starting at start
pred Delete[d, dPost: Doc, start, k: Int] {
  k > 0
  start >= 0
  plus[start, k] =< d.n

  -- positions before the deleted range: unchanged
  all i: Int | (i >= 0 and i < start) implies
    dPost.content[i] = d.content[i]

  -- positions after the deleted range: shifted down by k
  all i: Int | (i >= start and i < minus[d.n, k]) implies
    dPost.content[i] = d.content[plus[i, k]]

  -- nothing beyond the new end
  all i: Int | (i < 0 or i >= minus[d.n, k]) implies
    no dPost.content[i]
}

-- Property: resulting document length equals n_d - k
assert DeleteLength {
  all d, dPost: Doc, start, k: Int |
    Delete[d, dPost, start, k] implies
      dPost.n = minus[d.n, k]
}

check DeleteLength for 5 but exactly 2 Doc, 5 Int

-- Non-vacuity: a Delete on a document with at least 2 positions
run FindDelete {
  some d, dPost: Doc, start, k: Int |
    Delete[d, dPost, start, k] and d.n > 1
} for 5 but exactly 2 Doc, 5 Int
