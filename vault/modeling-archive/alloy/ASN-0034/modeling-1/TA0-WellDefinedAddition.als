-- TA0-WellDefinedAddition.als
-- TA0: For tumblers a, w where w > 0 and actionPoint(w) <= #a,
-- the result a + w is a well-defined tumbler in T.

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
  all i: Int {
    (i >= 1 and i =< len) implies one comp[i]
    (i < 1 or i > len) implies no comp[i]
  }
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- Bound input components to prevent integer overflow.
-- With 5-bit signed Int (range -16..15) and components <= 7,
-- the maximum sum at the action point is 14, within range.
pred bounded[t: Tumbler] {
  all i: Int | some t.comp[i] implies t.comp[i] =< 7
}

pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] != 0
}

pred isActionPoint[w: Tumbler, k: Int] {
  k >= 1
  k =< w.len
  w.comp[k] != 0
  all j: Int | (j >= 1 and j < k) implies w.comp[j] = 0
}

pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isPositive[w]
  isActionPoint[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | i >= 1 and i =< r.len implies {
    (i < k) implies r.comp[i] = a.comp[i]
    (i = k) implies r.comp[i] = plus[a.comp[k], w.comp[k]]
    (i > k) implies r.comp[i] = w.comp[i]
  }
}

-- TA0: the constructed result satisfies tumbler well-formedness
assert WellDefinedAddition {
  all a, w: Tumbler, k: Int |
    (bounded[a] and bounded[w] and isActionPoint[w, k] and k =< a.len)
    implies {
      -- result length is positive
      w.len >= 1
      -- action-point sum is non-negative
      plus[a.comp[k], w.comp[k]] >= 0
      -- prefix components from a are non-negative
      all i: Int | (i >= 1 and i < k) implies a.comp[i] >= 0
      -- suffix components from w are non-negative
      all i: Int | (i > k and i =< w.len) implies w.comp[i] >= 0
    }
}

-- Determinism: the result is uniquely determined
assert UniqueResult {
  all a, w, r1, r2: Tumbler, k: Int |
    (tumblerAdd[a, w, r1, k] and tumblerAdd[a, w, r2, k])
    implies
    (r1.len = r2.len and r1.comp = r2.comp)
}

-- Non-vacuity: a valid addition instance exists
run NonVacuity {
  some a, w, r: Tumbler, k: Int |
    bounded[a] and bounded[w] and tumblerAdd[a, w, r, k]
} for 5 but exactly 3 Tumbler, 5 Int

check WellDefinedAddition for 5 but 5 Int
check UniqueResult for 5 but exactly 4 Tumbler, 5 Int
