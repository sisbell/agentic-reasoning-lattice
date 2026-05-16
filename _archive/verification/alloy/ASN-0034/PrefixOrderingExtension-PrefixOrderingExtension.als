open util/integer

sig Tumbler {
  len: Int,
  elem: Int -> lone Int
} {
  len >= 1
  all i: Int | (i >= 1 and i =< len) iff some elem[i]
  all i: Int | some elem[i] implies elem[i] >= 0
}

-- Lexicographic less-than (T1): case (i) divergence, case (ii) proper prefix
pred ltTumbler[a, b: Tumbler] {
  {
    some k: Int {
      k >= 1
      k =< a.len
      k =< b.len
      a.elem[k] < b.elem[k]
      all i: Int | (i >= 1 and i < k) implies a.elem[i] = b.elem[i]
    }
  }
  or
  {
    a.len < b.len
    all i: Int | (i >= 1 and i =< a.len) implies a.elem[i] = b.elem[i]
  }
}

-- Prefix-or-equal: p is a prefix of a (p ≼ a)
pred isPrefix[p, a: Tumbler] {
  p.len =< a.len
  all i: Int | (i >= 1 and i =< p.len) implies p.elem[i] = a.elem[i]
}

-- Property: if p1 < p2 and neither is a prefix of the other,
-- then every extension of p1 is less than every extension of p2
assert PrefixOrderingExtension {
  all p1, p2, a, b: Tumbler |
    (ltTumbler[p1, p2]
     and not isPrefix[p1, p2]
     and not isPrefix[p2, p1]
     and isPrefix[p1, a]
     and isPrefix[p2, b])
    implies ltTumbler[a, b]
}

-- Non-vacuity: the preconditions are satisfiable
run NonVacuity {
  some p1, p2, a, b: Tumbler {
    ltTumbler[p1, p2]
    not isPrefix[p1, p2]
    not isPrefix[p2, p1]
    isPrefix[p1, a]
    isPrefix[p2, b]
  }
} for 5 but 5 Int

check PrefixOrderingExtension for 5 but 5 Int
