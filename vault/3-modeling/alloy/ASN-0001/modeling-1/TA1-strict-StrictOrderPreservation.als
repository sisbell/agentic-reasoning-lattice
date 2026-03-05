open util/integer

-- Tumbler: hierarchical address with three non-negative integer components
-- (1-indexed positions 1, 2, 3 in the spec).
sig Tumbler {
  c1, c2, c3: Int
}

-- Components are natural numbers, bounded to keep addition within Int range.
fact NonNegativeAndBounded {
  all t: Tumbler |
    t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0 and
    t.c1 =< 4 and t.c2 =< 4 and t.c3 =< 4
}

-- Positive tumbler: at least one component is nonzero.
pred positive[t: Tumbler] {
  not (t.c1 = 0) or not (t.c2 = 0) or not (t.c3 = 0)
}

-- Action point: 1-indexed position of first nonzero component.
-- Returns empty set when t is the zero tumbler.
fun actionPoint[w: Tumbler]: Int {
  { k: Int |
    (k = 1 and not (w.c1 = 0)) or
    (k = 2 and w.c1 = 0 and not (w.c2 = 0)) or
    (k = 3 and w.c1 = 0 and w.c2 = 0 and not (w.c3 = 0))
  }
}

-- Divergence: first 1-indexed position where a and b differ.
-- Returns empty set when a = b component-wise.
fun divergence[a, b: Tumbler]: Int {
  { k: Int |
    (k = 1 and not (a.c1 = b.c1)) or
    (k = 2 and a.c1 = b.c1 and not (a.c2 = b.c2)) or
    (k = 3 and a.c1 = b.c1 and a.c2 = b.c2 and not (a.c3 = b.c3))
  }
}

-- Lexicographic strict ordering on Tumblers.
pred lt[a, b: Tumbler] {
  a.c1 < b.c1 or
  (a.c1 = b.c1 and a.c2 < b.c2) or
  (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

-- TumblerAdd component functions for a ⊕ w, where k = actionPoint[w]:
--   rᵢ = aᵢ       if i < k   (copy from start)
--   rᵢ = aₖ + wₖ  if i = k   (advance)
--   rᵢ = wᵢ       if i > k   (copy from displacement)

fun addC1[a, w: Tumbler]: Int {
  { v: Int |
    (actionPoint[w] = 1 and v = plus[a.c1, w.c1]) or
    (not (actionPoint[w] = 1) and v = a.c1)
  }
}

fun addC2[a, w: Tumbler]: Int {
  { v: Int |
    (actionPoint[w] = 1 and v = w.c2) or
    (actionPoint[w] = 2 and v = plus[a.c2, w.c2]) or
    (actionPoint[w] = 3 and v = a.c2)
  }
}

fun addC3[a, w: Tumbler]: Int {
  { v: Int |
    (actionPoint[w] = 3 and v = plus[a.c3, w.c3]) or
    (not (actionPoint[w] = 3) and v = w.c3)
  }
}

-- TA1-strict — StrictOrderPreservation (POST)
-- If a < b, w > 0, and actionPoint(w) >= divergence(a, b), then a ⊕ w < b ⊕ w.
--
-- Intuition: let d = divergence(a, b) and k = actionPoint(w).
--   Positions < d: a and b agree, both results copy identically.
--   Position d (= divergence): a_d < b_d.
--     If d < k: both results copy aᵢ / bᵢ at position d, so result_d(a) < result_d(b).
--     If d = k: advance rule gives a_d + w_k vs b_d + w_k; since a_d < b_d the order holds.
--   Positions > d (when d = k): both results copy from w identically.
assert StrictOrderPreservation {
  all a, b, w: Tumbler |
    (lt[a, b] and positive[w] and actionPoint[w] >= divergence[a, b])
    implies
    (let ra1 = addC1[a, w], ra2 = addC2[a, w], ra3 = addC3[a, w],
         rb1 = addC1[b, w], rb2 = addC2[b, w], rb3 = addC3[b, w] |
     ra1 < rb1 or
     (ra1 = rb1 and ra2 < rb2) or
     (ra1 = rb1 and ra2 = rb2 and ra3 < rb3))
}

-- Non-vacuity: precondition is satisfiable (e.g. a=[0,0,1], b=[0,0,2], w=[0,0,1]).
run NonVacuous {
  some a, b, w: Tumbler |
    lt[a, b] and positive[w] and actionPoint[w] >= divergence[a, b]
} for 5 but 5 Int

check StrictOrderPreservation for 5 but 5 Int
