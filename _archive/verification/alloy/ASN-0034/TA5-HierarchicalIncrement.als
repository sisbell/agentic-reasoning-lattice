open util/integer

-- Tumbler: finite sequence of natural numbers
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

pred wellFormed[t: Tumbler] {
  t.len >= 1
  all i: Int | (i >= 1 and i =< t.len) implies one i.(t.comp)
  all i: Int | (i < 1 or i > t.len) implies no i.(t.comp)
  all i: Int | (i >= 1 and i =< t.len) implies t.comp[i] >= 0
}

fact { all t: Tumbler | wellFormed[t] }

-- TA5-SIG: last significant position (rightmost nonzero, or len if all zero)
pred isSigPos[t: Tumbler, s: Int] {
  s >= 1
  s =< t.len
  all j: Int | (j > s and j =< t.len) implies t.comp[j] = 0
  t.comp[s] != 0 or
    (s = t.len and (all j: Int | (j >= 1 and j =< t.len) implies t.comp[j] = 0))
}

-- T1: lexicographic less-than
pred lt[a: Tumbler, b: Tumbler] {
  -- Case (i): first difference within shared length, a component smaller
  (some d: Int |
    d >= 1 and d =< a.len and d =< b.len and
    a.comp[d] < b.comp[d] and
    (all i: Int | (i >= 1 and i < d) implies a.comp[i] = b.comp[i]))
  or
  -- Case (ii): a is proper prefix of b
  (a.len < b.len and
    (all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]))
}

-- TA5: inc(t, k) construction
pred Inc[t: Tumbler, k: Int, tPrime: Tumbler] {
  k >= 0
  -- k = 0 (sibling): increment at sig(t)
  k = 0 implies (some s: Int |
    isSigPos[t, s] and
    tPrime.len = t.len and
    tPrime.comp[s] = plus[t.comp[s], 1] and
    (all i: Int | (i >= 1 and i =< t.len and i != s) implies
      tPrime.comp[i] = t.comp[i]))
  -- k > 0 (child): extend by k positions
  k > 0 implies (
    tPrime.len = plus[t.len, k] and
    (all i: Int | (i >= 1 and i =< t.len) implies
      tPrime.comp[i] = t.comp[i]) and
    (all i: Int | (i > t.len and i < plus[t.len, k]) implies
      tPrime.comp[i] = 0) and
    tPrime.comp[plus[t.len, k]] = 1)
}

-- Postcondition (a): t' > t under T1
assert IncStrictlyGreater {
  all t, tPrime: Tumbler, k: Int |
    Inc[t, k, tPrime] implies lt[t, tPrime]
}

-- Postcondition (b): agreement before increment point
assert IncAgreement {
  all t, tPrime: Tumbler, k: Int |
    Inc[t, k, tPrime] implies {
      k = 0 implies (all s: Int | isSigPos[t, s] implies
        (all i: Int | (i >= 1 and i < s) implies
          tPrime.comp[i] = t.comp[i]))
      k > 0 implies
        (all i: Int | (i >= 1 and i =< t.len) implies
          tPrime.comp[i] = t.comp[i])
    }
}

-- Postcondition (c): sibling structure — same length, only sig(t) modified
assert IncSiblingStructure {
  all t, tPrime: Tumbler, k: Int |
    (k = 0 and Inc[t, k, tPrime]) implies (
      tPrime.len = t.len and
      (all s: Int | isSigPos[t, s] implies
        tPrime.comp[s] = plus[t.comp[s], 1]))
}

-- Postcondition (d): child structure — extended length, separators, final 1
assert IncChildStructure {
  all t, tPrime: Tumbler, k: Int |
    (k > 0 and Inc[t, k, tPrime]) implies (
      tPrime.len = plus[t.len, k] and
      (all i: Int | (i > t.len and i < plus[t.len, k]) implies
        tPrime.comp[i] = 0) and
      tPrime.comp[plus[t.len, k]] = 1)
}

-- Non-vacuity: sibling increment
run FindSiblingInc {
  some t, tPrime: Tumbler |
    Inc[t, 0, tPrime]
} for 4 but exactly 2 Tumbler, 5 Int

-- Non-vacuity: child increment
run FindChildInc {
  some t, tPrime: Tumbler, k: Int |
    k > 0 and Inc[t, k, tPrime]
} for 4 but exactly 2 Tumbler, 5 Int

check IncStrictlyGreater for 5 but exactly 2 Tumbler, 5 Int
check IncAgreement for 5 but exactly 2 Tumbler, 5 Int
check IncSiblingStructure for 5 but exactly 2 Tumbler, 5 Int
check IncChildStructure for 5 but exactly 2 Tumbler, 5 Int
