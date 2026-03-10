-- ASN-0027 / A2.compact — DeleteCompaction (POST, ensures)
-- Property: (A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))
-- After deleting k positions starting at p, positions beyond the deleted
-- range compact leftward by k: for each original position j in [start+k, n),
-- the post-state at j-k equals the pre-state at j.

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

-- A2.compact in original formulation: iterate over OLD positions j in
-- [start+k, n) and check that the post-state at j-k equals pre-state at j
assert DeleteCompaction {
  all d, dPost: Doc, start, k: Int |
    Delete[d, dPost, start, k] implies
      (all j: Int | (j >= plus[start, k] and j < d.n) implies
        dPost.content[minus[j, k]] = d.content[j])
}

check DeleteCompaction for 5 but exactly 2 Doc, 5 Int

-- Non-vacuity: a Delete on a document with at least 2 positions
run FindDelete {
  some d, dPost: Doc, start, k: Int |
    Delete[d, dPost, start, k] and d.n > 1
} for 5 but exactly 2 Doc, 5 Int
