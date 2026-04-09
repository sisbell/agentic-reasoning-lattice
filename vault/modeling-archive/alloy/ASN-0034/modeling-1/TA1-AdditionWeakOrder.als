open util/integer

-- Tumbler: sequence of non-negative integers, max length 3
sig Tumbler {
  len: Int,
  c1: Int,
  c2: Int,
  c3: Int
} {
  len >= 1
  len =< 3
  c1 >= 0
  c2 >= 0
  c3 >= 0
  len < 2 implies c2 = 0
  len < 3 implies c3 = 0
}

-- Component at position i (0 if out of range)
fun comp[t: Tumbler, i: Int]: Int {
  (i = 1) => t.c1 else ((i = 2) => t.c2 else ((i = 3) => t.c3 else 0))
}

-- Positive: at least one nonzero component
pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and comp[t, i] > 0
}

-- Action point: first nonzero position
pred isActionPoint[w: Tumbler, k: Int] {
  k >= 1
  k =< w.len
  comp[w, k] > 0
  all i: Int | (i >= 1 and i < k) implies comp[w, i] = 0
}

-- Strict tumbler order: a < b via divergence
pred tumblerLT[a, b: Tumbler] {
  some k: Int {
    k >= 1
    -- all positions before k agree
    all i: Int | (i >= 1 and i < k) implies
      (i =< a.len and i =< b.len and comp[a, i] = comp[b, i])
    -- divergence at k
    {
      -- component divergence
      k =< a.len and k =< b.len and comp[a, k] < comp[b, k]
    } or {
      -- prefix divergence: a is proper prefix of b
      a.len < b.len and k = plus[a.len, 1]
    }
  }
}

-- Weak tumbler order: a <= b (structural equality or strict LT)
pred tumblerLE[a, b: Tumbler] {
  (a.len = b.len and a.c1 = b.c1 and a.c2 = b.c2 and a.c3 = b.c3)
  or tumblerLT[a, b]
}

-- Tumbler addition: r = a + w with action point k
-- Result length = #w; positions <k from a, position k summed, positions >k from w
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPoint[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | (i >= 1 and i =< r.len) implies {
    (i < k) implies comp[r, i] = comp[a, i]
    (i = k) implies comp[r, i] = plus[comp[a, k], comp[w, k]]
    (i > k) implies comp[r, i] = comp[w, i]
  }
}

-- TA1: a < b and w > 0 and k <= min(#a,#b) implies a+w <= b+w
assert AdditionWeakOrder {
  all a, b, w, aw, bw: Tumbler, k: Int |
    (tumblerLT[a, b] and isPositive[w] and isActionPoint[w, k]
     and k =< a.len and k =< b.len
     and tumblerAdd[a, w, aw, k] and tumblerAdd[b, w, bw, k])
    implies tumblerLE[aw, bw]
}

-- Non-vacuity
run NonVacuity {
  some disj a, b, w, aw, bw: Tumbler |
    some k: Int |
      tumblerLT[a, b] and isPositive[w] and isActionPoint[w, k]
      and k =< a.len and k =< b.len
      and tumblerAdd[a, w, aw, k] and tumblerAdd[b, w, bw, k]
} for 5 but exactly 5 Tumbler, 5 Int

check AdditionWeakOrder for 5 but 5 Int
