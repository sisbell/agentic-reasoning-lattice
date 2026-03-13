-- TA1-strict: AdditionStrictOrder (LEMMA)
-- For a < b, w > 0, k = actionPoint(w), k <= min(#a,#b), k >= divergence(a,b):
--   a (+) w < b (+) w

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fact TumblerWellFormed {
  all t: Tumbler {
    t.len >= 1
    t.len =< 3
    all i: Int {
      (1 =< i and i =< t.len) implies
        (one t.comp[i] and t.comp[i] >= 0 and t.comp[i] =< 7)
      (i < 1 or i > t.len) implies no t.comp[i]
    }
  }
}

-- Tumbler strict ordering (T1)
pred tumblerLT[a, b: Tumbler] {
  -- Case 1: component divergence at a shared position
  (some k: Int {
    1 =< k and k =< a.len and k =< b.len
    a.comp[k] < b.comp[k]
    all i: Int | (1 =< i and i < k) implies a.comp[i] = b.comp[i]
  })
  or
  -- Case 2: a is a proper prefix of b
  (a.len < b.len and
   all i: Int | (1 =< i and i =< a.len) implies a.comp[i] = b.comp[i])
}

-- Positive tumbler: at least one nonzero component
pred positive[t: Tumbler] {
  some i: Int | 1 =< i and i =< t.len and t.comp[i] > 0
}

-- Action point: first nonzero component of a positive tumbler
pred isActionPoint[w: Tumbler, k: Int] {
  1 =< k and k =< w.len
  w.comp[k] > 0
  all i: Int | (1 =< i and i < k) implies w.comp[i] = 0
}

-- Divergence point of two distinct tumblers
pred isDivergence[a, b: Tumbler, d: Int] {
  -- Case 1: component divergence
  {
    1 =< d and d =< a.len and d =< b.len
    not (a.comp[d] = b.comp[d])
    all i: Int | (1 =< i and i < d) implies a.comp[i] = b.comp[i]
  }
  or
  -- Case 2: prefix divergence
  {
    d = plus[min[a.len + b.len], 1]
    not (a.len = b.len)
    all i: Int | (1 =< i and i =< min[a.len + b.len]) implies a.comp[i] = b.comp[i]
  }
}

-- Tumbler addition: r = a (+) w, with action point k
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPoint[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | (1 =< i and i =< r.len) implies {
    (i < k) implies r.comp[i] = a.comp[i]
    (i = k) implies r.comp[i] = plus[a.comp[k], w.comp[k]]
    (i > k) implies r.comp[i] = w.comp[i]
  }
}

-- TA1-strict: addition preserves strict order under the given conditions
assert AdditionStrictOrder {
  all a, b, w, aw, bw: Tumbler | all k, d: Int |
    (tumblerLT[a, b] and positive[w] and
     isActionPoint[w, k] and isDivergence[a, b, d] and
     k =< min[a.len + b.len] and k >= d and
     tumblerAdd[a, w, aw, k] and tumblerAdd[b, w, bw, k])
    implies
      tumblerLT[aw, bw]
}

-- Non-vacuity: confirm the preconditions are satisfiable
run NonVacuity {
  some disj a, b, w, aw, bw: Tumbler | some k, d: Int |
    tumblerLT[a, b] and positive[w] and
    isActionPoint[w, k] and isDivergence[a, b, d] and
    k =< min[a.len + b.len] and k >= d and
    tumblerAdd[a, w, aw, k] and tumblerAdd[b, w, bw, k] and
    tumblerLT[aw, bw]
} for 5 but exactly 5 Tumbler, 5 Int

check AdditionStrictOrder for 5 but exactly 5 Tumbler, 5 Int
