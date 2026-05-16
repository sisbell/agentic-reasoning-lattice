open util/integer

-- Tumbler with up to 3 components (sufficient for bounded check)
-- c0 always present; c1, c2 optional (determines length 1, 2, or 3)
sig Tumbler {
  c0: Int,
  c1: lone Int,
  c2: lone Int
}

fun tlen[t: Tumbler]: Int {
  (some t.c2) => 3 else ((some t.c1) => 2 else 1)
}

fact WellFormed {
  all t: Tumbler {
    t.c0 >= 0
    some t.c1 implies t.c1 >= 0
    some t.c2 implies (t.c2 >= 0 and some t.c1)
  }
}

-- shift(orig, n) = orig + delta(n, #orig)
-- Per OrdinalShift and TumblerAdd with action point m = #orig:
--   prefix (indices 1..m-1) preserved
--   last component (index m) increased by n
--   length preserved
pred isShift[result, orig: Tumbler, n: Int] {
  n >= 1
  tlen[result] = tlen[orig]
  tlen[orig] = 1 implies {
    result.c0 = plus[orig.c0, n]
  }
  tlen[orig] = 2 implies {
    result.c0 = orig.c0
    result.c1 = plus[orig.c1, n]
  }
  tlen[orig] = 3 implies {
    result.c0 = orig.c0
    result.c1 = orig.c1
    result.c2 = plus[orig.c2, n]
  }
}

pred tumblerEq[a, b: Tumbler] {
  a.c0 = b.c0 and a.c1 = b.c1 and a.c2 = b.c2
}

-- TS3 (ShiftComposition): shift(shift(v, n1), n2) = shift(v, n1 + n2)
assert ShiftComposition {
  all v, u, w, r: Tumbler, n1, n2: Int |
    (n1 >= 1 and n2 >= 1 and
     isShift[u, v, n1] and
     isShift[w, u, n2] and
     isShift[r, v, plus[n1, n2]])
    implies
    tumblerEq[w, r]
}

-- Frame: composed shift preserves tumbler length
assert ShiftCompositionPreservesLength {
  all v, u, w: Tumbler, n1, n2: Int |
    (n1 >= 1 and n2 >= 1 and
     isShift[u, v, n1] and
     isShift[w, u, n2])
    implies
    tlen[w] = tlen[v]
}

-- Non-vacuity: the constraints are satisfiable
run NonVacuity {
  some v, u, w, r: Tumbler, n1, n2: Int |
    n1 >= 1 and n2 >= 1 and
    isShift[u, v, n1] and
    isShift[w, u, n2] and
    isShift[r, v, plus[n1, n2]]
} for 5 but exactly 4 Tumbler, 5 Int

check ShiftComposition for 5 but exactly 4 Tumbler, 5 Int
check ShiftCompositionPreservesLength for 5 but exactly 4 Tumbler, 5 Int
