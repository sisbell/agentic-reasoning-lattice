-- PrefixOrderingExtension: if p1 < p2 (lexicographic) and neither
-- is a prefix of the other, then every extension of p1 is less than
-- every extension of p2.

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 5
  all i: Int | (i >= 0 and i < len) iff some comp[i]
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- Component value at position i, treating out-of-range as 0
fun compAt[t: Tumbler, i: Int]: one Int {
  (i >= 0 and i < t.len) => t.comp[i] else 0
}

-- p is a prefix of a (p ≼ a)
pred isPrefix[p: Tumbler, a: Tumbler] {
  p.len =< a.len
  all i: Int | (i >= 0 and i < p.len) implies p.comp[i] = a.comp[i]
}

-- Lexicographic strict ordering (a < b)
-- At the divergence point, a's component is strictly less than b's;
-- all earlier positions agree (missing components treated as 0).
pred lexLT[a: Tumbler, b: Tumbler] {
  some k: Int {
    k >= 0
    compAt[a, k] < compAt[b, k]
    all j: Int | (j >= 0 and j < k) implies compAt[a, j] = compAt[b, j]
  }
}

assert PrefixOrderingExtension {
  all p1, p2, a, b: Tumbler |
    (lexLT[p1, p2]
     and not isPrefix[p1, p2] and not isPrefix[p2, p1]
     and isPrefix[p1, a] and isPrefix[p2, b])
    implies lexLT[a, b]
}

-- Non-vacuity: premises are simultaneously satisfiable
run NonVacuity {
  some disj p1, p2, a, b: Tumbler |
    lexLT[p1, p2]
    and not isPrefix[p1, p2] and not isPrefix[p2, p1]
    and isPrefix[p1, a] and p1 != a
    and isPrefix[p2, b] and p2 != b
} for 5 but 4 Int

check PrefixOrderingExtension for 5 but 4 Int
