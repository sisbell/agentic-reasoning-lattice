-- TS2-ShiftInjectivity.als
-- Property: shift(v1, n) = shift(v2, n) implies v1 = v2
-- for equal-length tumblers v1, v2 and n >= 1

open util/integer

-- A tumbler: finite sequence of non-negative integers, 1-indexed
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  all i: Int | (1 =< i and i =< len) implies one comp[i]
  all i: Int | (i < 1 or i > len) implies no comp[i]
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- Mathematical equality of tumblers (same length and components)
pred tumblerEq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | a.comp[i] = b.comp[i]
}

-- shift(v, n) = v ⊕ δ(n, #v)
-- δ(n, m) = [0,...,0,n] of length m, actionPoint = m
-- By TumblerAdd with action point k = m:
--   rᵢ = vᵢ for i < m
--   rₘ = vₘ + n
--   no positions i > m (since #δ = m = #v)
--   #result = #δ = m
pred isShift[v, result: Tumbler, n: Int] {
  n >= 1
  result.len = v.len
  all i: Int | (1 =< i and i < v.len) implies
    result.comp[i] = v.comp[i]
  result.comp[v.len] = plus[v.comp[v.len], n]
}

-- TS2: ShiftInjectivity
-- Preconditions: v1, v2 in T, n >= 1, #v1 = #v2 = m
-- Postcondition: shift(v1, n) = shift(v2, n) implies v1 = v2
assert ShiftInjectivity {
  all v1, v2, r1, r2: Tumbler, n: Int |
    (n >= 1 and v1.len = v2.len
     and isShift[v1, r1, n]
     and isShift[v2, r2, n]
     and tumblerEq[r1, r2])
    implies tumblerEq[v1, v2]
}

-- Non-vacuity: a valid shift instance exists
run NonVacuity {
  some v, result: Tumbler, n: Int |
    n >= 1 and isShift[v, result, n]
} for 3 but exactly 2 Tumbler, 4 Int

check ShiftInjectivity for 4 but exactly 4 Tumbler, 4 Int
