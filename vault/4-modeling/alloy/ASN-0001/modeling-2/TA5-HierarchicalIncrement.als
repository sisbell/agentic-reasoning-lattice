open util/integer

-- Tumbler: finite sequence of non-negative integers
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 7
  all i: Int | (i >= 1 and i =< len) implies (one comp[i] and comp[i] >= 0)
  all i: Int | (i < 1 or i > len) implies no comp[i]
}

-- Component with zero-padding beyond length
fun padComp[t: Tumbler, i: Int]: Int {
  (i >= 1 and i =< t.len) => t.comp[i] else 0
}

-- Last significant position: rightmost nonzero, or len if all zero
fun sigPos[t: Tumbler]: Int {
  let nz = {i: Int | i >= 1 and i =< t.len and t.comp[i] > 0} |
    some nz => max[nz] else t.len
}

-- Number of zero-valued components
fun zeroCount[t: Tumbler]: Int {
  #{i: Int | i >= 1 and i =< t.len and t.comp[i] = 0}
}

-- Lexicographic strict less-than with zero-padding
pred lexLT[a, b: Tumbler] {
  let ml = (a.len >= b.len => a.len else b.len) |
    some k: Int {
      k >= 1
      k =< ml
      all j: Int | (j >= 1 and j < k) implies padComp[a, j] = padComp[b, j]
      padComp[a, k] < padComp[b, k]
    }
}

-- Sibling increment (k = 0): bump the last significant position by 1
pred incSibling[t, tPrime: Tumbler] {
  let s = sigPos[t] {
    tPrime.len = t.len
    tPrime.comp[s] = plus[t.comp[s], 1]
    all i: Int | (i >= 1 and i =< t.len and not (i = s)) implies
      tPrime.comp[i] = t.comp[i]
  }
}

-- Child increment (k > 0): extend with k-1 zero separators and a 1
pred incChild[t, tPrime: Tumbler, k: Int] {
  k >= 1
  tPrime.len = plus[t.len, k]
  all i: Int | (i >= 1 and i =< t.len) implies
    tPrime.comp[i] = t.comp[i]
  all i: Int | (i > t.len and i < plus[t.len, k]) implies
    tPrime.comp[i] = 0
  tPrime.comp[plus[t.len, k]] = 1
}

-- Combined increment operation
pred inc[t, tPrime: Tumbler, k: Int] {
  k >= 0
  k = 0 implies incSibling[t, tPrime]
  k > 0 implies incChild[t, tPrime, k]
}

-- TA5(a): Result is strictly greater under lexicographic order
assert IncStrictlyGreater {
  all t, tPrime: Tumbler, k: Int |
    inc[t, tPrime, k] implies lexLT[t, tPrime]
}

-- TA5(b): Agreement before the increment point
assert IncAgreesPrefix {
  all t, tPrime: Tumbler, k: Int |
    inc[t, tPrime, k] implies {
      k = 0 implies
        (all i: Int | (i >= 1 and i < sigPos[t]) implies
          tPrime.comp[i] = t.comp[i])
      k > 0 implies
        (all i: Int | (i >= 1 and i =< t.len) implies
          tPrime.comp[i] = t.comp[i])
    }
}

-- TA5 preserves T4: zero count stays within 3 when precondition holds
assert IncPreservesT4 {
  all t, tPrime: Tumbler, k: Int |
    (inc[t, tPrime, k] and plus[zeroCount[t], minus[k, 1]] =< 3)
      implies zeroCount[tPrime] =< 3
}

-- Non-vacuity: sibling increment is satisfiable
run FindSibling {
  some t, tPrime: Tumbler |
    incSibling[t, tPrime]
} for 5 but exactly 2 Tumbler, 5 Int

-- Non-vacuity: child increment is satisfiable
run FindChild {
  some t, tPrime: Tumbler, k: Int |
    k >= 1 and incChild[t, tPrime, k]
} for 5 but exactly 2 Tumbler, 5 Int

check IncStrictlyGreater for 5 but exactly 2 Tumbler, 5 Int
check IncAgreesPrefix for 5 but exactly 2 Tumbler, 5 Int
check IncPreservesT4 for 5 but exactly 2 Tumbler, 5 Int
