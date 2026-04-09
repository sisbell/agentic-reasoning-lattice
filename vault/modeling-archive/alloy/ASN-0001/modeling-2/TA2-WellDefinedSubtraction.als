open util/integer

-- Tumblers modeled with 3 components (fixed-length, zero-padded representation).
-- Variable-length tumblers are captured by trailing zeros.
sig Tumbler {
  c0: one Int,
  c1: one Int,
  c2: one Int
}

-- A tumbler is valid iff all components are non-negative
pred validTumbler[t: Tumbler] {
  t.c0 >= 0
  t.c1 >= 0
  t.c2 >= 0
}

-- Lexicographic ordering: a >= w
-- At the first position where they differ, a's component is strictly greater;
-- or they are equal at all positions.
pred geq[a: Tumbler, w: Tumbler] {
  a.c0 > w.c0
  or (a.c0 = w.c0 and a.c1 > w.c1)
  or (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 >= w.c2)
}

-- TumblerSubtract: r = a ⊖ w
-- At divergence point k: r[i<k]=0, r[k]=a[k]-w[k], r[i>k]=a[i]
-- When equal: result is zero tumbler
pred subtract[a: Tumbler, w: Tumbler, r: Tumbler] {
  -- Diverge at position 0
  (a.c0 != w.c0) implies
    (r.c0 = minus[a.c0, w.c0] and r.c1 = a.c1 and r.c2 = a.c2)

  -- Diverge at position 1
  (a.c0 = w.c0 and a.c1 != w.c1) implies
    (r.c0 = 0 and r.c1 = minus[a.c1, w.c1] and r.c2 = a.c2)

  -- Diverge at position 2
  (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 != w.c2) implies
    (r.c0 = 0 and r.c1 = 0 and r.c2 = minus[a.c2, w.c2])

  -- Equal: result is zero tumbler
  (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 = w.c2) implies
    (r.c0 = 0 and r.c1 = 0 and r.c2 = 0)
}

-- TA2: For valid tumblers a >= w, a ⊖ w is a valid tumbler
assert WellDefinedSubtraction {
  all a, w, r: Tumbler |
    (validTumbler[a] and validTumbler[w] and geq[a, w] and subtract[a, w, r])
    implies validTumbler[r]
}

-- Non-vacuity: a valid subtraction with distinct operands exists
run NonVacuity {
  some a, w, r: Tumbler |
    validTumbler[a] and validTumbler[w] and geq[a, w]
    and not (a.c0 = w.c0 and a.c1 = w.c1 and a.c2 = w.c2)
    and subtract[a, w, r]
} for 5 but exactly 3 Tumbler, 5 Int

check WellDefinedSubtraction for 5 but exactly 3 Tumbler, 5 Int
