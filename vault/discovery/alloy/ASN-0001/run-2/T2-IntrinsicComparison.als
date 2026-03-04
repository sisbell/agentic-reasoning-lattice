open util/integer

-- Tumbler: a finite sequence of non-negative integer components
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
  all i: Int | (i >= 1 and i =< len) iff one comp[i]
  all i: Int | one comp[i] implies comp[i] >= 0
}

-- Component accessor: returns value at position i, or 0 if out of range
fun getComp[t: Tumbler, i: Int]: Int {
  let v = t.comp[i] | (some v => v else 0)
}

-- Minimum of two integers
fun minInt[a, b: Int]: Int {
  (a =< b) => a else b
}

-- First position in 1..min(#a,#b) where components differ
pred divergesAt[a, b: Tumbler, k: Int] {
  k >= 1
  k =< minInt[a.len, b.len]
  not (getComp[a, k] = getComp[b, k])
  all i: Int | (i >= 1 and i < k) implies getComp[a, i] = getComp[b, i]
}

-- All components agree in the shared range 1..min(#a,#b)
pred agreeOnSharedRange[a, b: Tumbler] {
  all i: Int | (i >= 1 and i =< minInt[a.len, b.len]) implies
    getComp[a, i] = getComp[b, i]
}

-- Lexicographic less-than, defined purely from tumbler components
pred LessThan[a, b: Tumbler] {
  (some k: Int | divergesAt[a, b, k] and getComp[a, k] < getComp[b, k])
  or
  (agreeOnSharedRange[a, b] and a.len < b.len)
}

-- T2a: Comparison is intrinsic — determined entirely by component
-- sequences. Two pairs with identical sequences yield identical results.
assert IntrinsicComparison {
  all a1, a2, b1, b2: Tumbler |
    (a1.len = a2.len and b1.len = b2.len
     and (all i: Int | getComp[a1, i] = getComp[a2, i])
     and (all i: Int | getComp[b1, i] = getComp[b2, i]))
    implies
    (LessThan[a1, b1] iff LessThan[a2, b2])
}

-- T2b: Comparison examines at most min(#a, #b) positions.
-- Tumblers that agree on the shared range but differ beyond it
-- produce the same comparison result.
assert BoundedExamination {
  all a1, a2, b: Tumbler |
    (a1.len = a2.len
     and (all i: Int | (i >= 1 and i =< minInt[a1.len, b.len]) implies
            getComp[a1, i] = getComp[a2, i]))
    implies
    (LessThan[a1, b] iff LessThan[a2, b])
}

-- Non-vacuity: the model admits a pair where one is less than another
run NonVacuity {
  some a, b: Tumbler | LessThan[a, b]
} for 3 but exactly 2 Tumbler, 5 Int

check IntrinsicComparison for 4 but 5 Int
check BoundedExamination for 4 but 5 Int
