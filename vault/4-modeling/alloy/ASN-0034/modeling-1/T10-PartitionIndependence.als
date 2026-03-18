-- T10-PartitionIndependence.als
-- Partition independence: non-nesting prefixes yield distinct addresses.
--
-- Property: let p1 and p2 be prefixes such that neither is a prefix of
-- the other. Then for any tumbler a with prefix p1 and any tumbler b
-- with prefix p2, a != b (as sequences).

sig Tumbler {
  len: Int,
  val: Int -> lone Int
} {
  len >= 1
  all i: Int | (some val[i]) iff (i >= 1 and i =< len)
  all i: Int | (some val[i]) implies val[i] >= 0
}

-- Sequence equality: same length and same components at every position
pred sameSeq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.val[i] = b.val[i]
}

-- p is a prefix of t: p is no longer than t, and they agree on 1..#p
pred isPrefix[p, t: Tumbler] {
  p.len =< t.len
  all i: Int | (i >= 1 and i =< p.len) implies p.val[i] = t.val[i]
}

-- Neither prefix nests the other
pred nonNesting[p1, p2: Tumbler] {
  not isPrefix[p1, p2]
  not isPrefix[p2, p1]
}

-- T10: non-nesting prefixes guarantee distinct addresses
assert PartitionIndependence {
  all p1, p2, a, b: Tumbler |
    (nonNesting[p1, p2] and isPrefix[p1, a] and isPrefix[p2, b])
      implies not sameSeq[a, b]
}

-- Non-vacuity: the setup is satisfiable with proper extensions
run NonVacuity {
  some disj p1, p2, a, b: Tumbler |
    nonNesting[p1, p2] and isPrefix[p1, a] and isPrefix[p2, b]
} for 5 but exactly 4 Tumbler, 4 Int

check PartitionIndependence for 5 but 4 Int
