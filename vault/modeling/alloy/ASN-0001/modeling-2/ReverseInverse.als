open util/integer

-- ReverseInverse: (a ⊖ w) ⊕ w = a
-- Under: a >= w, w > 0, k = #a, #w = k, all components of a before k are zero.

sig Tumbler {
  len: one Int,
  c0: one Int,
  c1: one Int,
  c2: one Int
}

-- All tumblers are well-formed: non-negative, length in [1,3],
-- components beyond length are zero.
fact AllValid {
  all t: Tumbler {
    t.len >= 1 and t.len =< 3
    t.c0 >= 0 and t.c1 >= 0 and t.c2 >= 0
    t.len =< 1 implies t.c1 = 0
    t.len =< 2 implies t.c2 = 0
  }
}

pred positive[t: Tumbler] {
  t.c0 != 0 or t.c1 != 0 or t.c2 != 0
}

-- Lexicographic ordering: a >= w (zero-padded to 3 components)
pred geq[a: Tumbler, w: Tumbler] {
  a.c0 > w.c0
  or (a.c0 = w.c0 and a.c1 > w.c1)
  or (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 >= w.c2)
}

-- Action point: k is the first nonzero position in w (1-indexed)
pred isActionPt[w: Tumbler, k: Int] {
  k >= 1 and k =< 3
  k = 1 implies w.c0 != 0
  k = 2 implies w.c1 != 0
  k = 3 implies w.c2 != 0
  k >= 2 implies w.c0 = 0
  k >= 3 implies w.c1 = 0
  w.c0 != 0 implies k = 1
  (w.c0 = 0 and w.c1 != 0) implies k = 2
}

-- TumblerAdd: r = a ⊕ w with action point k
-- r[i<k]=a[i], r[k]=a[k]+w[k], r[i>k]=w[i]; r.len = w.len
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPt[w, k]
  k =< a.len
  r.len = w.len

  -- Position 1
  k = 1 implies r.c0 = plus[a.c0, w.c0]
  k != 1 implies r.c0 = a.c0

  -- Position 2 (within result length)
  (r.len >= 2 and k = 2) implies r.c1 = plus[a.c1, w.c1]
  (r.len >= 2 and k < 2) implies r.c1 = w.c1
  (r.len >= 2 and k > 2) implies r.c1 = a.c1

  -- Position 3 (within result length)
  (r.len >= 3 and k = 3) implies r.c2 = plus[a.c2, w.c2]
  (r.len >= 3 and k < 3) implies r.c2 = w.c2
}

-- TumblerSubtract: r = a ⊖ w (zero-padded to max length)
-- At divergence point: zero before, subtract at divergence, copy rest from a
pred tumblerSub[a, w, r: Tumbler] {
  -- Equal: zero tumbler
  (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 = w.c2) implies
    (r.c0 = 0 and r.c1 = 0 and r.c2 = 0)

  -- Diverge at position 1
  (a.c0 != w.c0) implies
    (r.c0 = minus[a.c0, w.c0] and r.c1 = a.c1 and r.c2 = a.c2)

  -- Diverge at position 2
  (a.c0 = w.c0 and a.c1 != w.c1) implies
    (r.c0 = 0 and r.c1 = minus[a.c1, w.c1] and r.c2 = a.c2)

  -- Diverge at position 3
  (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 != w.c2) implies
    (r.c0 = 0 and r.c1 = 0 and r.c2 = minus[a.c2, w.c2])

  -- Result length = max(a.len, w.len)
  (a.len >= w.len) implies r.len = a.len
  (w.len > a.len) implies r.len = w.len
}

-- ReverseInverse preconditions (same structural constraints as TA4)
pred riPre[a, w: Tumbler, k: Int] {
  positive[w]
  geq[a, w]
  isActionPt[w, k]
  k = a.len           -- action point at last component of a
  w.len = k           -- w has same length as a
  -- all components of a before k are zero
  k >= 2 implies a.c0 = 0
  k >= 3 implies a.c1 = 0
}

-- ReverseInverse: (a ⊖ w) ⊕ w = a
assert ReverseInverse {
  all a, w, d, r: Tumbler, k: Int |
    (riPre[a, w, k]
     and tumblerSub[a, w, d]
     and tumblerAdd[d, w, r, k]
     -- overflow guards for bounded Int arithmetic
     and minus[a.c0, w.c0] >= 0
     and minus[a.c1, w.c1] >= 0
     and minus[a.c2, w.c2] >= 0
     and plus[d.c0, w.c0] >= 0
     and plus[d.c1, w.c1] >= 0
     and plus[d.c2, w.c2] >= 0)
    implies
    (r.c0 = a.c0 and r.c1 = a.c1 and r.c2 = a.c2 and r.len = a.len)
}

-- Non-vacuity: satisfiable with a nonzero start position
run NonVacuity {
  some a, w, d, r: Tumbler, k: Int |
    riPre[a, w, k]
    and tumblerSub[a, w, d]
    and tumblerAdd[d, w, r, k]
    and minus[a.c0, w.c0] >= 0
    and minus[a.c1, w.c1] >= 0
    and minus[a.c2, w.c2] >= 0
    and plus[d.c0, w.c0] >= 0
    and plus[d.c1, w.c1] >= 0
    and plus[d.c2, w.c2] >= 0
    and positive[a]
} for 5 but exactly 4 Tumbler, 5 Int

check ReverseInverse for 5 but exactly 4 Tumbler, 5 Int
