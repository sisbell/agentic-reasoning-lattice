-- TA3 — SubtractionWeakOrder
-- Property: (A a, b, w : a < b ∧ a >= w ∧ b >= w : a ⊖ w <= b ⊖ w)
-- Subtraction by a common displacement preserves weak tumbler order.
--
-- Modeling: tumblers as 3-component vectors of non-negative integers.
-- Variable-length tumblers with zero-padding reduce to this fixed-length form.

open util/integer

sig Tumbler {
  c0: Int,
  c1: Int,
  c2: Int
}

fact NonNeg {
  all t: Tumbler | t.c0 >= 0 and t.c1 >= 0 and t.c2 >= 0
}

-- Lexicographic strict less-than
pred tLt[a, b: Tumbler] {
  a.c0 < b.c0
  or (a.c0 = b.c0 and a.c1 < b.c1)
  or (a.c0 = b.c0 and a.c1 = b.c1 and a.c2 < b.c2)
}

-- Lexicographic less-than-or-equal
pred tLeq[a, b: Tumbler] {
  a.c0 < b.c0
  or (a.c0 = b.c0 and a.c1 < b.c1)
  or (a.c0 = b.c0 and a.c1 = b.c1 and a.c2 =< b.c2)
}

-- Greater-than-or-equal (a >= w iff w <= a)
pred tGeq[a, b: Tumbler] {
  tLeq[b, a]
}

-- Tumbler subtraction: r = a ⊖ w
-- Find divergence point (first position where a and w differ),
-- zero positions before it, subtract at it, copy a after it.
pred isSub[r, a, w: Tumbler] {
  -- Divergence at position 0
  not (a.c0 = w.c0) implies
    (r.c0 = minus[a.c0, w.c0] and r.c1 = a.c1 and r.c2 = a.c2)
  -- Divergence at position 1
  (a.c0 = w.c0 and not (a.c1 = w.c1)) implies
    (r.c0 = 0 and r.c1 = minus[a.c1, w.c1] and r.c2 = a.c2)
  -- Divergence at position 2
  (a.c0 = w.c0 and a.c1 = w.c1 and not (a.c2 = w.c2)) implies
    (r.c0 = 0 and r.c1 = 0 and r.c2 = minus[a.c2, w.c2])
  -- No divergence (a = w)
  (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 = w.c2) implies
    (r.c0 = 0 and r.c1 = 0 and r.c2 = 0)
}

-- TA3: subtraction preserves weak order
assert SubtractionWeakOrder {
  all a, b, w, r1, r2: Tumbler |
    (tLt[a, b] and tGeq[a, w] and tGeq[b, w]
      and isSub[r1, a, w] and isSub[r2, b, w])
    implies tLeq[r1, r2]
}

-- Non-vacuity: preconditions are satisfiable
run NonVacuity {
  some disj a, b, w, r1, r2: Tumbler |
    tLt[a, b] and tGeq[a, w] and tGeq[b, w]
    and isSub[r1, a, w] and isSub[r2, b, w]
} for 5 but exactly 5 Tumbler, 5 Int

check SubtractionWeakOrder for 5 but exactly 5 Tumbler, 5 Int
