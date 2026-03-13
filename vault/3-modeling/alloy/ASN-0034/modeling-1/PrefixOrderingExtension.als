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

-- Prefix-or-equal: p is a prefix of a (p <= a)
pred isPrefix[p, a: Tumbler] {
  p.len =< a.len
  all i: Int | (i >= 1 and i =< p.len) implies p.comp[i] = a.comp[i]
}

-- Prefix ordering extension:
-- If p1 < p2 and neither is a prefix of the other,
-- then every extension of p1 is less than every extension of p2.
assert PrefixOrderingExtension {
  all p1, p2, a, b: Tumbler |
    (lt[p1, p2]
     and not isPrefix[p1, p2]
     and not isPrefix[p2, p1]
     and isPrefix[p1, a]
     and isPrefix[p2, b])
    implies lt[a, b]
}

-- Non-vacuity: find p1 < p2 (not prefix-related) with strict extensions
run NonVacuity {
  some disj p1, p2, a, b: Tumbler {
    lt[p1, p2]
    not isPrefix[p1, p2]
    not isPrefix[p2, p1]
    isPrefix[p1, a]
    isPrefix[p2, b]
    p1.len < a.len
    p2.len < b.len
  }
} for 5 but exactly 4 Tumbler, 5 Int

check PrefixOrderingExtension for 5 but 5 Int
