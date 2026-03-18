-- T2-IntrinsicComparison: tumbler ordering depends only on components
open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
  all i: Int | (some comp[i]) iff (i >= 1 and i =< len)
  all i: Int | (some comp[i]) implies comp[i] >= 0
}

-- T1 ordering: lexicographic with prefix extension
pred lessThan[a, b: Tumbler] {
  -- Case (i): component divergence
  (some k: Int {
    k >= 1
    k =< a.len
    k =< b.len
    all i: Int | (i >= 1 and i < k) implies a.comp[i] = b.comp[i]
    a.comp[k] < b.comp[k]
  })
  or
  -- Case (ii): a is a proper prefix of b
  (a.len < b.len and
   (all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]))
}

-- Two tumblers have identical component sequences
pred sameSequence[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]
}

-- T2a: comparison is intrinsic — same components yield same ordering
assert IntrinsicComparison {
  all a1, a2, b1, b2: Tumbler |
    (sameSequence[a1, a2] and sameSequence[b1, b2])
    implies
    (lessThan[a1, b1] iff lessThan[a2, b2])
}

-- T2b: at most min(#a, #b) component pairs determine the result
assert ComparisonBounded {
  all a1, a2, b1, b2: Tumbler |
    (a1.len = a2.len and b1.len = b2.len and
     (all i: Int |
       (i >= 1 and i =< a1.len and i =< b1.len) implies
       (a1.comp[i] = a2.comp[i] and b1.comp[i] = b2.comp[i])))
    implies
    (lessThan[a1, b1] iff lessThan[a2, b2])
}

-- Non-vacuity: distinct comparable tumblers exist
run NonVacuity {
  some a, b: Tumbler | a != b and lessThan[a, b]
} for 4 but exactly 2 Tumbler, 4 Int

check IntrinsicComparison for 5 but exactly 4 Tumbler, 4 Int
check ComparisonBounded for 5 but exactly 4 Tumbler, 4 Int
