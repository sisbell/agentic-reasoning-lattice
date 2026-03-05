-- T12 — SpanWellDefined
-- A span (s, l) with l > 0 denotes {t : s <= t < s ⊕ l}.
-- This set is contiguous under lexicographic order and non-empty.

open util/integer

sig Tumbler {
  c1: Int,
  c2: Int,
  c3: Int
}

-- All components are non-negative
fact NonNeg {
  all t: Tumbler | t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0
}

-- Lexicographic less-than-or-equal
pred leq[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 =< b.c3)
}

-- Strict lexicographic less-than
pred lt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

-- Positive: at least one nonzero component
pred positive[t: Tumbler] {
  t.c1 > 0 or t.c2 > 0 or t.c3 > 0
}

-- Action point: index of first nonzero component (1, 2, or 3)
fun actionPoint[w: Tumbler]: Int {
  (w.c1 > 0) => 1 else ((w.c2 > 0) => 2 else 3)
}

-- Tumbler addition: result = a ⊕ w
-- For 3-component tumblers with action point k:
--   k=1: [a1+w1, w2, w3]   (advance at level 1, tail from w)
--   k=2: [a1, a2+w2, w3]   (copy a1, advance at level 2, tail from w)
--   k=3: [a1, a2, a3+w3]   (copy a1-a2, advance at level 3)
pred tumblerAdd[a, w, result: Tumbler] {
  positive[w]
  let k = actionPoint[w] {
    k = 1 implies (
      result.c1 = plus[a.c1, w.c1] and
      result.c2 = w.c2 and
      result.c3 = w.c3
    )
    k = 2 implies (
      result.c1 = a.c1 and
      result.c2 = plus[a.c2, w.c2] and
      result.c3 = w.c3
    )
    k = 3 implies (
      result.c1 = a.c1 and
      result.c2 = a.c2 and
      result.c3 = plus[a.c3, w.c3]
    )
  }
}

-- Membership in span [s, endpoint) where endpoint = s ⊕ l
pred inSpan[t, s, endpoint: Tumbler] {
  leq[s, t] and lt[t, endpoint]
}

-- Contiguity: nothing between two span members is outside the span
assert SpanContiguous {
  all s, l, endpoint, t1, t2, t3: Tumbler |
    (positive[l] and tumblerAdd[s, l, endpoint]
     and inSpan[t1, s, endpoint]
     and inSpan[t2, s, endpoint]
     and leq[t1, t3] and leq[t3, t2])
    implies inSpan[t3, s, endpoint]
}

-- Non-emptiness: s itself is in its own span [s, s ⊕ l)
assert SpanNonEmpty {
  all s, l, endpoint: Tumbler |
    (positive[l] and tumblerAdd[s, l, endpoint])
    implies inSpan[s, s, endpoint]
}

-- Strict increase: s ⊕ l > s when l > 0
assert StrictIncrease {
  all s, l, endpoint: Tumbler |
    (positive[l] and tumblerAdd[s, l, endpoint])
    implies lt[s, endpoint]
}

-- Non-vacuity: find a span with a member other than s
run FindSpan {
  some s, l, endpoint, t: Tumbler |
    positive[l] and tumblerAdd[s, l, endpoint]
    and inSpan[t, s, endpoint] and t != s
} for 5 but 6 Int

check SpanContiguous for 5 but 6 Int
check SpanNonEmpty for 5 but 6 Int
check StrictIncrease for 5 but 6 Int
