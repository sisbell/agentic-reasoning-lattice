-- TS1: ShiftOrderPreservation
-- For v1, v2 in T with #v1 = #v2 = m, v1 < v2, and n >= 1:
-- shift(v1, n) < shift(v2, n)

open util/integer

sig Tumbler {
  elems: seq Int
}

-- Tumbler components are non-negative natural numbers
fact NonNegativeComponents {
  all t: Tumbler, i: Int | some t.elems[i] implies t.elems[i] >= 0
}

-- Tumblers are non-empty (length >= 1)
fact NonEmpty {
  all t: Tumbler | #t.elems >= 1
}

-- Tumbler length
fun len[t: Tumbler]: Int {
  #t.elems
}

-- Lexicographic strict less-than for equal-length tumblers
-- Divergence case (i): first index k where a_k != b_k, with a_k < b_k
pred ltTumbler[a, b: Tumbler] {
  len[a] = len[b]
  some k: Int {
    some a.elems[k]
    a.elems[k] < b.elems[k]
    all j: Int | (some a.elems[j] and j < k) implies a.elems[j] = b.elems[j]
  }
}

-- OrdinalShift via TumblerAdd with displacement delta(n, m) = [0,...,0,n]
-- actionPoint(delta(n,m)) = m, so addition touches only the last component:
--   result_i = t_i for i < m;  result_m = t_m + n
pred isShift[t: Tumbler, n: Int, result: Tumbler] {
  len[result] = len[t]
  let lastIdx = minus[len[t], 1] {
    result.elems[lastIdx] = plus[t.elems[lastIdx], n]
    all i: Int | (some t.elems[i] and not (i = lastIdx))
      implies result.elems[i] = t.elems[i]
  }
}

-- Guard against integer overflow in bounded Alloy arithmetic
pred shiftSafe[t: Tumbler, n: Int] {
  let lastIdx = minus[len[t], 1] |
    plus[t.elems[lastIdx], n] >= t.elems[lastIdx]
}

-- TS1: ShiftOrderPreservation
assert ShiftOrderPreservation {
  all v1, v2, s1, s2: Tumbler, n: Int |
    (n >= 1 and len[v1] = len[v2] and ltTumbler[v1, v2]
     and isShift[v1, n, s1] and isShift[v2, n, s2]
     and shiftSafe[v1, n] and shiftSafe[v2, n])
    implies ltTumbler[s1, s2]
}

-- Non-vacuity: confirm preconditions are satisfiable
run NonVacuity {
  some v1, v2, s1, s2: Tumbler, n: Int |
    n >= 1 and len[v1] = len[v2] and ltTumbler[v1, v2]
    and isShift[v1, n, s1] and isShift[v2, n, s2]
    and shiftSafe[v1, n] and shiftSafe[v2, n]
} for 4 but exactly 4 Tumbler, 3 seq, 5 Int

check ShiftOrderPreservation for 4 but exactly 4 Tumbler, 3 seq, 5 Int
