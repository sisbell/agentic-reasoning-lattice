-- StrictIncrease (TA-strict): a ⊕ w > a when w > 0
--
-- For all tumblers a and positive displacements w, tumbler
-- addition produces a result strictly greater than the start.

sig Tumbler {
  comp : Int -> lone Int,
  len  : one Int
}

fact TumblerWellFormed {
  all t: Tumbler {
    t.len >= 1
    t.len =< 4
    all i: Int {
      (i >= 1 and i =< t.len) implies
        (one t.comp[i] and t.comp[i] >= 0 and t.comp[i] =< 7)
      (i < 1 or i > t.len) implies no t.comp[i]
    }
  }
}

-- Positive tumbler: at least one nonzero component
pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] != 0
}

-- Action point: first nonzero position of w
pred isActionPoint[w: Tumbler, k: Int] {
  k >= 1
  k =< w.len
  w.comp[k] != 0
  all i: Int | (i >= 1 and i < k) implies w.comp[i] = 0
}

-- Component value, zero-padded beyond length
fun getComp[t: Tumbler, i: Int]: Int {
  (i >= 1 and i =< t.len) => t.comp[i] else 0
}

-- Tumbler addition: r = a ⊕ w with action point k
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPoint[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | (i >= 1 and i =< w.len) implies {
    (i < k)  implies r.comp[i] = a.comp[i]
    (i = k)  implies r.comp[i] = plus[a.comp[k], w.comp[k]]
    (i > k)  implies r.comp[i] = w.comp[i]
  }
}

-- Lexicographic strict order
pred tumblerGT[a, b: Tumbler] {
  some k: Int {
    k >= 1
    all i: Int | (i >= 1 and i < k) implies getComp[a, i] = getComp[b, i]
    getComp[a, k] > getComp[b, k]
  }
}

-- Property: tumbler addition with positive displacement strictly increases
assert StrictIncrease {
  all a, w, r: Tumbler, k: Int |
    (isPositive[w] and tumblerAdd[a, w, r, k]) implies tumblerGT[r, a]
}

-- Non-vacuity: a valid addition exists
run NonVacuity {
  some disj a, w, r: Tumbler, k: Int |
    isPositive[w] and tumblerAdd[a, w, r, k]
} for 5 but exactly 3 Tumbler, 5 Int

check StrictIncrease for 5 but exactly 3 Tumbler, 5 Int
