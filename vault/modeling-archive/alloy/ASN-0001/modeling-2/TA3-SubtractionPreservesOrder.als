open util/integer

-- Tumblers modeled with 3 components (fixed-length, zero-padded representation).
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

-- Strict lexicographic ordering: a < b (zero-padded to 3 components)
pred lt[a: Tumbler, b: Tumbler] {
  a.c0 < b.c0
  or (a.c0 = b.c0 and a.c1 < b.c1)
  or (a.c0 = b.c0 and a.c1 = b.c1 and a.c2 < b.c2)
}

-- Lexicographic ordering: a >= w
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

-- TA3: Subtraction preserves strict order
-- (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w < b ⊖ w)
assert SubtractionPreservesOrder {
  all a, b, w, aw, bw: Tumbler |
    (validTumbler[a] and validTumbler[b] and validTumbler[w]
     and lt[a, b] and geq[a, w] and geq[b, w]
     and subtract[a, w, aw] and subtract[b, w, bw])
    implies lt[aw, bw]
}

-- Non-vacuity: premises are satisfiable with distinct a < b
run NonVacuity {
  some a, b, w, aw, bw: Tumbler |
    validTumbler[a] and validTumbler[b] and validTumbler[w]
    and lt[a, b] and geq[a, w] and geq[b, w]
    and subtract[a, w, aw] and subtract[b, w, bw]
} for 5 but exactly 5 Tumbler, 5 Int

check SubtractionPreservesOrder for 5 but exactly 5 Tumbler, 5 Int
