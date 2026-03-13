open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 5
  all p: Int | (p >= 1 and p =< len) iff some comp[p]
  all p: Int | some comp[p] implies comp[p] >= 0
}

-- Lexicographic strict order (T1)
-- a < b iff there exists k >= 1 with all positions before k agreeing, and either:
--   (i) component divergence: k <= min(#a,#b) and a_k < b_k, or
--   (ii) prefix: k = #a + 1 <= #b (a is a proper prefix of b)
pred lt[a, b: Tumbler] {
  some k: Int {
    k >= 1
    all i: Int | (i >= 1 and i < k) implies a.comp[i] = b.comp[i]
    {
      k =< a.len and k =< b.len and a.comp[k] < b.comp[k]
    } or {
      k = plus[a.len, 1] and k =< b.len
    }
  }
}

-- Extensional equality of tumblers
pred eq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | a.comp[i] = b.comp[i]
}

-- Irreflexivity: no tumbler is less than itself
assert Irreflexive {
  all a: Tumbler | not lt[a, a]
}

-- Extensional irreflexivity: extensionally equal tumblers are not ordered
assert ExtIrreflexive {
  all a, b: Tumbler | eq[a, b] implies not lt[a, b]
}

-- Asymmetry: a < b implies not b < a
assert Asymmetric {
  all a, b: Tumbler | lt[a, b] implies not lt[b, a]
}

-- Transitivity: a < b and b < c implies a < c
assert Transitive {
  all a, b, c: Tumbler |
    (lt[a, b] and lt[b, c]) implies lt[a, c]
}

-- Totality: distinct tumblers are comparable
assert Total {
  all a, b: Tumbler | (not eq[a, b]) implies (lt[a, b] or lt[b, a])
}

-- Non-vacuity: the ordering is satisfiable
run NonVacuity {
  some a, b: Tumbler | lt[a, b]
} for 4 but exactly 2 Tumbler

check Irreflexive for 5
check ExtIrreflexive for 5
check Asymmetric for 5
check Transitive for 5 but exactly 3 Tumbler
check Total for 5
