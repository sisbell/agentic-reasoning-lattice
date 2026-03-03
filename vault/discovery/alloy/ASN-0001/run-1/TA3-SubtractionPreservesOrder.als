-- TA3: SubtractionPreservesOrder
-- (A a, b, w : a < b ∧ a ≥ w ∧ b ≥ w : a ⊖ w < b ⊖ w)
--
-- Modeled with 2-component tumblers; components are non-negative integers.
-- Ordering is lexicographic. Subtraction is defined by divergence point k.

sig Tumbler {
  c1: Int,
  c2: Int
}

fact NonNegative {
  all t: Tumbler | t.c1 >= 0 and t.c2 >= 0
}

-- Strict lexicographic order: a < b.
pred lt[a, b: Tumbler] {
  (a.c1 < b.c1)
  or
  (a.c1 = b.c1 and a.c2 < b.c2)
}

-- Reflexive lexicographic order: a <= b.
pred lte[a, b: Tumbler] {
  lt[a, b] or (a.c1 = b.c1 and a.c2 = b.c2)
}

-- TumblerSubtract: r = a ⊖ w.
-- Cases are on divergence point k (first position where a and w differ).
-- Caller is responsible for precondition lte[w, a].
pred Subtract[a, w, r: Tumbler] {
  -- k = 1: first components differ → r = (a₁ − w₁, a₂)
  (not (a.c1 = w.c1)) implies
    (r.c1 = minus[a.c1, w.c1] and r.c2 = a.c2)

  -- k = 2: first components equal, second differ → r = (0, a₂ − w₂)
  (a.c1 = w.c1 and not (a.c2 = w.c2)) implies
    (r.c1 = 0 and r.c2 = minus[a.c2, w.c2])

  -- a = w: zero result
  (a.c1 = w.c1 and a.c2 = w.c2) implies
    (r.c1 = 0 and r.c2 = 0)
}

-- TA3: subtraction preserves strict order.
assert SubtractionPreservesOrder {
  all a, b, w, ra, rb: Tumbler |
    (lt[a, b] and lte[w, a] and lte[w, b] and
     Subtract[a, w, ra] and Subtract[b, w, rb])
    implies lt[ra, rb]
}

-- Non-vacuity: find a witness where the full antecedent holds.
run SubtractWitness {
  some a, b, w, ra, rb: Tumbler |
    lt[a, b] and lte[w, a] and lte[w, b] and
    Subtract[a, w, ra] and Subtract[b, w, rb] and
    lt[ra, rb]
} for 5 but 4 Int

check SubtractionPreservesOrder for 5 but 4 Int
