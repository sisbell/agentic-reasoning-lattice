-- T12-SpanWellDefined
-- Bounded Alloy check for T12 (SpanWellDefined).
-- A span (s, len) with len > 0 denotes the set {t : s <= t < s ⊕ len}.
-- Verified: (a) the span is non-empty; (b) the span is contiguous.
--
-- Model: 2-component tumblers [c0, c1] over bounded natural numbers.
-- Lexicographic order on ℕ² models the T1 tumbler ordering.
-- TumblerAdd is instantiated for 2-component tumblers (Defn TumblerAdd).

sig Tumbler {
  c0: Int,
  c1: Int
}

-- Non-negative components, bounded to prevent arithmetic overflow
fact WellFormed {
  all t: Tumbler {
    t.c0 >= 0 and t.c0 =< 3
    t.c1 >= 0 and t.c1 =< 3
  }
}

-- Positive tumbler: at least one nonzero component (Defn PositiveTumbler)
pred positive[t: Tumbler] {
  t.c0 != 0 or t.c1 != 0
}

-- Lexicographic order: a <= b  (T1 ordering restricted to ℕ²)
pred leq[a, b: Tumbler] {
  a.c0 < b.c0 or (a.c0 = b.c0 and a.c1 =< b.c1)
}

-- Strict lexicographic order: a < b
pred lt[a, b: Tumbler] {
  a.c0 < b.c0 or (a.c0 = b.c0 and a.c1 < b.c1)
}

-- TumblerAdd: r = a ⊕ w  (Defn TumblerAdd, 2-component case)
-- Action point k of w:
--   k=1 when w.c0 != 0 : r = [a.c0 + w.c0, w.c1]
--   k=2 when w.c0=0, w.c1!=0 : r = [a.c0, a.c1 + w.c1]
-- Both components of r are fully determined when positive[w].
pred isAdd[a, w, r: Tumbler] {
  w.c0 != 0 implies {
    r.c0 = plus[a.c0, w.c0]
    r.c1 = w.c1
  }
  (w.c0 = 0 and w.c1 != 0) implies {
    r.c0 = a.c0
    r.c1 = plus[a.c1, w.c1]
  }
}

-- T12a (TAStrict): Adding a positive displacement strictly advances position.
-- This is TA-strict: s < s ⊕ len whenever len > 0.
-- Implication: s itself is always in the span [s, s⊕len), so the span is non-empty.
assert TAStrict {
  all s, len, end: Tumbler |
    (positive[len] and isAdd[s, len, end]) implies lt[s, end]
}

-- T12b (SpanContiguous): The half-open interval [s, s⊕len) is convex.
-- Any tumbler between two span members is itself a span member.
-- Argument: s <= t1 <= t3 <= t2 < end implies s <= t3 < end by transitivity.
assert SpanContiguous {
  all s, len, end, t1, t2, t3: Tumbler |
    (positive[len] and isAdd[s, len, end]
     and leq[s, t1] and lt[t1, end]
     and leq[s, t2] and lt[t2, end]
     and leq[t1, t3] and leq[t3, t2])
    implies (leq[s, t3] and lt[t3, end])
}

-- Non-vacuity: find a span containing two distinct positions
run FindSpan {
  some s, len: Tumbler | some disj t1, t2: Tumbler |
    positive[len] and lt[t1, t2] and
    (some end: Tumbler | isAdd[s, len, end] and leq[s, t1] and lt[t1, end]) and
    (some end: Tumbler | isAdd[s, len, end] and leq[s, t2] and lt[t2, end])
} for 6 but 5 Int

check TAStrict for 6 but 5 Int
check SpanContiguous for 6 but 5 Int
