-- T1 — LexicographicOrder
-- Strict lexicographic order on tumblers (sequences of natural numbers).
-- Checks: irreflexive, asymmetric, transitive, total (trichotomy).

sig Tumbler {
  comps: seq Int
}

-- Tumbler components are natural numbers (non-negative integers)
fact NonNegative {
  all t: Tumbler, i: t.comps.inds | t.comps[i] >= 0
}

-- Strict lexicographic less-than.
-- k is 0-based (spec T1 uses 1-based; k here = k_spec - 1).
-- a < b iff some k >= 0 such that:
--   (prefix) all i in [0, k): a[i] = b[i]
--   (i)      k in both lengths and a[k] < b[k], OR
--   (ii)     k = len(a) and k < len(b)  -- a is a proper prefix of b
pred lexLT[a, b: Tumbler] {
  some k: Int | {
    k >= 0
    all i: Int | (i >= 0 and i < k) implies a.comps[i] = b.comps[i]
    (
      (k < #a.comps and k < #b.comps and a.comps[k] < b.comps[k])
      or
      (k = #a.comps and k < #b.comps)
    )
  }
}

-- Irreflexivity: no tumbler is less than itself
assert Irreflexive {
  no t: Tumbler | lexLT[t, t]
}

-- Asymmetry: a < b implies not (b < a)
assert Asymmetric {
  all a, b: Tumbler | lexLT[a, b] implies not lexLT[b, a]
}

-- Transitivity: a < b and b < c implies a < c
assert Transitive {
  all a, b, c: Tumbler |
    (lexLT[a, b] and lexLT[b, c]) implies lexLT[a, c]
}

-- Trichotomy: tumblers with distinct component sequences are ordered
-- (uses sequence equality, not atom identity, to avoid spurious violations)
assert Trichotomy {
  all a, b: Tumbler |
    (a.comps != b.comps) implies (lexLT[a, b] or lexLT[b, a])
}

-- Non-vacuity: confirm the ordering relation is satisfiable
run FindLT {
  some a, b: Tumbler | lexLT[a, b]
} for 4 but exactly 2 Tumbler, 3 seq, 5 Int

check Irreflexive for 4 but 3 Tumbler, 3 seq, 5 Int
check Asymmetric for 4 but 3 Tumbler, 3 seq, 5 Int
check Transitive for 4 but 3 Tumbler, 3 seq, 5 Int
check Trichotomy for 4 but 3 Tumbler, 3 seq, 5 Int
