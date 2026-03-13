-- TA3-strict: SubtractionStrictOrder
-- (A a, b, w : a < b and a >= w and b >= w and #a = #b : a ⊖ w < b ⊖ w)
-- Fixed-length 3 tumblers; trailing zeros model shorter lengths.

open util/integer

sig Tumbler {
  c1: Int,
  c2: Int,
  c3: Int
} {
  c1 >= 0
  c2 >= 0
  c3 >= 0
}

pred tumblerLt[a, b: Tumbler] {
  a.c1 < b.c1
  or (a.c1 = b.c1 and a.c2 < b.c2)
  or (a.c1 = b.c1 and a.c2 = b.c2 and a.c3 < b.c3)
}

pred tumblerGeq[a, b: Tumbler] {
  not tumblerLt[a, b]
}

-- Components of a ⊖ w (tumbler subtraction)
fun subC1[a, w: Tumbler]: Int {
  not (a.c1 = w.c1) => minus[a.c1, w.c1] else 0
}

fun subC2[a, w: Tumbler]: Int {
  not (a.c1 = w.c1) => a.c2
  else (not (a.c2 = w.c2) => minus[a.c2, w.c2] else 0)
}

fun subC3[a, w: Tumbler]: Int {
  not (a.c1 = w.c1) => a.c3
  else (not (a.c2 = w.c2) => a.c3
  else (not (a.c3 = w.c3) => minus[a.c3, w.c3] else 0))
}

-- Strict less-than on computed subtraction results
pred subtractLt[a, w, b: Tumbler] {
  let ra1 = subC1[a, w], ra2 = subC2[a, w], ra3 = subC3[a, w],
      rb1 = subC1[b, w], rb2 = subC2[b, w], rb3 = subC3[b, w] |
    ra1 < rb1
    or (ra1 = rb1 and ra2 < rb2)
    or (ra1 = rb1 and ra2 = rb2 and ra3 < rb3)
}

assert TA3strict {
  all a, b, w: Tumbler |
    (tumblerLt[a, b] and tumblerGeq[a, w] and tumblerGeq[b, w])
    implies subtractLt[a, w, b]
}

run NonVacuity {
  some disj a, b, w: Tumbler |
    tumblerLt[a, b] and tumblerGeq[a, w] and tumblerGeq[b, w]
    and subtractLt[a, w, b]
} for 4 but exactly 3 Tumbler, 5 Int

check TA3strict for 4 but 5 Int
