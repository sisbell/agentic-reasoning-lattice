open util/integer

-- Tumbler: finite sequence of non-negative integers, 1-indexed
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  -- comp defined exactly on positions 1..len
  all i: Int | some comp[i] iff (i >= 1 and i =< len)
  -- component values are non-negative
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- p is a prefix of t: #p <= #t and components agree on 1..#p
pred isPrefix[p: Tumbler, t: Tumbler] {
  p.len =< t.len
  all i: Int | (i >= 1 and i =< p.len) implies t.comp[i] = p.comp[i]
}

-- Structural equality: same length and same components at every position
pred tumblerEq[a: Tumbler, b: Tumbler] {
  a.len = b.len
  all i: Int | a.comp[i] = b.comp[i]
}

-- T10 (PartitionIndependence): non-nesting prefixes guarantee distinct tumblers
-- Preconditions: p1, p2 in T with p1 not-prefix-of p2 and p2 not-prefix-of p1;
--                a, b in T with p1 prefix-of a and p2 prefix-of b
-- Postcondition: a != b
assert PartitionIndependence {
  all p1, p2, a, b: Tumbler |
    (not isPrefix[p1, p2] and not isPrefix[p2, p1]
     and isPrefix[p1, a] and isPrefix[p2, b])
    implies not tumblerEq[a, b]
}

-- Non-vacuity: preconditions are satisfiable
run NonVacuity {
  some disj p1, p2, a, b: Tumbler |
    not isPrefix[p1, p2] and not isPrefix[p2, p1]
    and isPrefix[p1, a] and isPrefix[p2, b]
} for 5 but 4 Int

check PartitionIndependence for 5 but 4 Int
