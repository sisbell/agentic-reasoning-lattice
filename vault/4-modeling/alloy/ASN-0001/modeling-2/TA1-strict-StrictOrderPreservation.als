-- TA1-strict: StrictOrderPreservation
-- If a < b, w > 0, and action point of w >= divergence(a,b),
-- then a + w < b + w.

open util/integer

sig Tumbler {
  len: Int,
  c1: Int,
  c2: Int,
  c3: Int
} {
  len >= 1
  len =< 3
  c1 >= 0 and c1 =< 7
  c2 >= 0 and c2 =< 7
  c3 >= 0 and c3 =< 7
  len < 2 implies c2 = 0
  len < 3 implies c3 = 0
}

-- Positive tumbler: at least one nonzero component
pred positive[t: Tumbler] {
  t.c1 != 0 or t.c2 != 0 or t.c3 != 0
}

-- Lexicographic strict ordering (zero-padded to 3 components)
pred lt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

-- First position where a and b differ (precondition: a != b)
fun divergence[a, b: Tumbler]: Int {
  (a.c1 != b.c1) => 1 else ((a.c2 != b.c2) => 2 else 3)
}

-- First nonzero component position (precondition: positive[w])
fun actionPoint[w: Tumbler]: Int {
  (w.c1 != 0) => 1 else ((w.c2 != 0) => 2 else 3)
}

-- Tumbler addition: result = a + w
-- At action point k: add. Before k: copy from a. After k: copy from w.
-- Result length = #w.
pred tumblerAdd[a, w, result: Tumbler] {
  let k = actionPoint[w] | {
    -- Precondition: action point within start position's length
    k =< a.len
    -- Result length equals displacement length
    result.len = w.len

    -- Position 1
    k = 1 implies result.c1 = plus[a.c1, w.c1]
    k != 1 implies result.c1 = a.c1

    -- Position 2
    k = 2 implies result.c2 = plus[a.c2, w.c2]
    k < 2 implies result.c2 = w.c2
    k > 2 implies result.c2 = a.c2

    -- Position 3
    k = 3 implies result.c3 = plus[a.c3, w.c3]
    k < 3 implies result.c3 = w.c3
  }
}

-- TA1-strict: strict order is preserved by addition
assert StrictOrderPreservation {
  all a, b, w, aw, bw: Tumbler |
    (lt[a, b] and positive[w] and
     actionPoint[w] >= divergence[a, b] and
     tumblerAdd[a, w, aw] and tumblerAdd[b, w, bw])
    implies lt[aw, bw]
}

-- Non-vacuity: premises are satisfiable
run NonVacuity {
  some a, b, w, aw, bw: Tumbler |
    lt[a, b] and positive[w] and
    actionPoint[w] >= divergence[a, b] and
    tumblerAdd[a, w, aw] and tumblerAdd[b, w, bw]
} for 5 but 5 Int

check StrictOrderPreservation for 6 but 5 Int
