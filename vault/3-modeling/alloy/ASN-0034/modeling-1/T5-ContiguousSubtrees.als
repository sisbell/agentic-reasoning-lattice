open util/integer

sig Tumbler {
  len: Int,
  c1: Int,
  c2: Int,
  c3: Int,
  c4: Int
} {
  1 =< len and len =< 4
  c1 >= 0 and c2 >= 0 and c3 >= 0 and c4 >= 0
  c1 =< 3 and c2 =< 3 and c3 =< 3 and c4 =< 3
}

-- component accessor: position -> value
fun comp[t: Tumbler]: Int -> Int {
  (1 -> t.c1) + (2 -> t.c2) + (3 -> t.c3) + (4 -> t.c4)
}

-- tumbler value equality (distinct atoms may encode the same tumbler)
pred tEq[a: Tumbler, b: Tumbler] {
  a.len = b.len
  all i: Int | (1 =< i and i =< a.len) implies comp[a][i] = comp[b][i]
}

-- p is a prefix of t (p ≼ t)
pred isPrefix[p: Tumbler, t: Tumbler] {
  p.len =< t.len
  all i: Int | (1 =< i and i =< p.len) implies comp[p][i] = comp[t][i]
}

-- strict T1 ordering: lexicographic with prefix rule
pred tLess[a: Tumbler, b: Tumbler] {
  -- a is a proper prefix of b
  (isPrefix[a, b] and not (a.len = b.len))
  or
  -- component divergence: a_k < b_k at first differing position
  (some k: Int {
    1 =< k and k =< a.len and k =< b.len
    comp[a][k] < comp[b][k]
    all i: Int | (1 =< i and i < k) implies comp[a][i] = comp[b][i]
  })
}

-- non-strict T1 ordering
pred tLeq[a: Tumbler, b: Tumbler] {
  tEq[a, b] or tLess[a, b]
}

-- T5: prefix-defined subtrees are contiguous intervals
assert ContiguousSubtrees {
  all p, a, b, c: Tumbler |
    (isPrefix[p, a] and isPrefix[p, c] and tLeq[a, b] and tLeq[b, c])
    implies isPrefix[p, b]
}

check ContiguousSubtrees for 5 but 5 Int

-- non-vacuity: the premise of T5 is satisfiable with distinct ordered tumblers
run NonVacuity {
  some p, a, b, c: Tumbler |
    isPrefix[p, a] and isPrefix[p, c] and
    tLess[a, b] and tLess[b, c]
} for 5 but 5 Int
