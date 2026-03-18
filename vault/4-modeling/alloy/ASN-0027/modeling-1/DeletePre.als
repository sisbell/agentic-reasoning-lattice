-- A2.pre — DeletePre (PRE)
-- Precondition: d ∈ Σ.D ∧ 1 ≤ p ∧ p + k − 1 ≤ n_d ∧ k ≥ 1

sig Doc {}

sig State {
  docs: set Doc,
  len: Doc -> lone Int
}

pred wellFormed[s: State] {
  all d: s.docs | one s.len[d] and s.len[d] >= 1
  all d: Doc - s.docs | no s.len[d]
}

pred DeletePre[s: State, d: Doc, p: Int, k: Int] {
  d in s.docs
  p >= 1
  k >= 1
  plus[p, minus[k, 1]] =< s.len[d]
}

-- Guard: plus[p, minus[k,1]] did not overflow
-- When k >= 1 and p >= 1, non-overflow implies plus[p, minus[k,1]] >= p
pred safeArith[p: Int, k: Int] {
  minus[k, 1] >= 0
  plus[p, minus[k, 1]] >= p
}

-- Start position is within document bounds
assert StartInBounds {
  all s: State, d: Doc, p: Int, k: Int |
    (wellFormed[s] and DeletePre[s, d, p, k] and safeArith[p, k]) implies
      p =< s.len[d]
}

-- End position is at least 1
assert EndAtLeastOne {
  all s: State, d: Doc, p: Int, k: Int |
    (wellFormed[s] and DeletePre[s, d, p, k] and safeArith[p, k]) implies
      plus[p, minus[k, 1]] >= 1
}

-- After deletion, remaining length is non-negative
assert RemainingNonNegative {
  all s: State, d: Doc, p: Int, k: Int |
    (wellFormed[s] and DeletePre[s, d, p, k] and safeArith[p, k]) implies
      minus[s.len[d], k] >= 0
}

run NonVacuity {
  some s: State, d: Doc, p: Int, k: Int |
    wellFormed[s] and DeletePre[s, d, p, k] and safeArith[p, k]
} for 4 but exactly 1 State, 5 Int

check StartInBounds for 5 but exactly 1 State, 5 Int
check EndAtLeastOne for 5 but exactly 1 State, 5 Int
check RemainingNonNegative for 5 but exactly 1 State, 5 Int
