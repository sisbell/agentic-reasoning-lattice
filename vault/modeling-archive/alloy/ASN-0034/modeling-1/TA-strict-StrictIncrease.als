open util/integer

-- Tumbler: variable-length sequence of natural numbers (max length 4)
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
  all i: Int | (i >= 1 and i =< len) implies one comp[i]
  all i: Int | (i < 1 or i > len) implies no comp[i]
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- A tumbler is positive iff at least one component is nonzero
pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] > 0
}

-- Action point: first nonzero component of displacement w
pred actionPoint[w: Tumbler, k: Int] {
  k >= 1
  k =< w.len
  w.comp[k] > 0
  all i: Int | (i >= 1 and i < k) implies w.comp[i] = 0
}

-- TumblerAdd: r = a + w with action point k
pred isAdd[a, w, r: Tumbler, k: Int] {
  actionPoint[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | (i >= 1 and i =< r.len) implies {
    (i < k) implies r.comp[i] = a.comp[i]
    (i = k) implies r.comp[i] = plus[a.comp[k], w.comp[k]]
    (i > k) implies r.comp[i] = w.comp[i]
  }
}

-- Effective equality at position i (treating beyond-length as 0)
pred effEq[a, b: Tumbler, i: Int] {
  (i =< a.len and i =< b.len) implies a.comp[i] = b.comp[i]
  (i =< a.len and i > b.len) implies a.comp[i] = 0
  (i > a.len and i =< b.len) implies b.comp[i] = 0
}

-- Tumbler ordering: a > b (lexicographic with zero-padding)
pred tGreater[a, b: Tumbler] {
  some k: Int {
    k >= 1
    k =< a.len or k =< b.len
    all i: Int | (i >= 1 and i < k) implies effEq[a, b, i]
    (k =< a.len and k =< b.len and a.comp[k] > b.comp[k])
    or (k =< a.len and k > b.len and a.comp[k] > 0)
  }
}

-- TA-strict: adding a positive displacement strictly increases
assert StrictIncrease {
  all a, w, r: Tumbler, k: Int |
    (isPositive[w] and isAdd[a, w, r, k]) implies tGreater[r, a]
}

-- Non-vacuity: confirm a valid Add instance exists
run NonVacuity {
  some a, w, r: Tumbler, k: Int |
    isPositive[w] and isAdd[a, w, r, k]
} for 5 but exactly 3 Tumbler, 5 Int

check StrictIncrease for 5 but exactly 3 Tumbler, 5 Int
