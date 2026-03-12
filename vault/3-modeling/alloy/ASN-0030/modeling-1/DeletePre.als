-- ASN-0030 A4 pre — DeletePre
-- Precondition for DELETE(d, p, k):
--   d ∈ Σ.D ∧ 1 ≤ p ∧ p + k − 1 ≤ n_d ∧ k ≥ 1

sig Document {}

sig State {
  docs: set Document,
  len: Document -> lone Int
} {
  -- len is defined exactly on docs
  len.Int = docs
  -- bound lengths to avoid integer overflow at 6-bit width
  all d: docs | d.len >= 0 and d.len =< 15
}

-- DELETE precondition (with overflow guard)
pred DeletePre[s: State, d: Document, p, k: Int] {
  d in s.docs
  p >= 1
  k >= 1
  let rangeEnd = plus[p, minus[k, 1]] {
    -- overflow guard: adding a non-negative value cannot decrease p
    rangeEnd >= p
    rangeEnd =< d.(s.len)
  }
}

-- Deletion count does not exceed document length
assert DeleteBounded {
  all s: State, d: Document, p, k: Int |
    DeletePre[s, d, p, k] implies k =< d.(s.len)
}

-- Post-deletion length is non-negative
assert PostLengthNonNeg {
  all s: State, d: Document, p, k: Int |
    DeletePre[s, d, p, k] implies minus[d.(s.len), k] >= 0
}

-- Start position is within document bounds
assert StartInRange {
  all s: State, d: Document, p, k: Int |
    DeletePre[s, d, p, k] implies p =< d.(s.len)
}

-- Non-vacuity: a valid DELETE precondition exists
run FindDelete {
  some s: State, d: Document, p, k: Int |
    DeletePre[s, d, p, k]
} for 4 but exactly 1 State, 6 Int

check DeleteBounded for 5 but exactly 1 State, 6 Int
check PostLengthNonNeg for 5 but exactly 1 State, 6 Int
check StartInRange for 5 but exactly 1 State, 6 Int
