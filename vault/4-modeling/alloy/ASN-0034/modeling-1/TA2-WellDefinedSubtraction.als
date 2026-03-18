open util/integer

-- Tumbler: finite sequence of natural-number components, 1-indexed
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  all i: Int {
    (1 =< i and i =< len) implies (one comp[i] and comp[i] >= 0)
    (i < 1 or i > len) implies no comp[i]
  }
}

-- Limit length to keep search space tractable
fact BoundedLength { all t: Tumbler | t.len =< 4 }

-- Padded component access: 0 beyond length
fun padded[t: Tumbler, i: Int]: one Int {
  (some t.comp[i]) => t.comp[i] else 0
}

-- Maximum of two tumbler lengths
fun maxLen[a: Tumbler, b: Tumbler]: one Int {
  max[a.len + b.len]
}

-- Padded equality: all positions agree after conceptual zero-padding
pred paddedEqual[a: Tumbler, b: Tumbler] {
  let ml = maxLen[a, b] |
    all i: Int | (1 =< i and i =< ml) implies padded[a, i] = padded[b, i]
}

-- Divergence: first position where padded values differ
pred isDivergence[a: Tumbler, b: Tumbler, k: Int] {
  1 =< k and k =< maxLen[a, b]
  not (padded[a, k] = padded[b, k])
  all j: Int | (1 =< j and j < k) implies padded[a, j] = padded[b, j]
}

-- Tumbler ordering: a >= w
pred geq[a: Tumbler, w: Tumbler] {
  paddedEqual[a, w]
  or
  (some k: Int | isDivergence[a, w, k] and padded[a, k] >= padded[w, k])
}

-- TA2: When a >= w, subtraction a - w is well-defined.
-- Result components: 0 before k (non-negative), a_k - w_k at k (check), a_i after k (non-negative by invariant).
-- The only non-trivial part: at the divergence point, a_k - w_k >= 0.
assert WellDefinedSubtraction {
  all a, w: Tumbler | geq[a, w] implies {
    maxLen[a, w] >= 1
    (not paddedEqual[a, w]) implies
      (all k: Int | isDivergence[a, w, k] implies
        minus[padded[a, k], padded[w, k]] >= 0)
  }
}

-- Non-vacuity: find distinct tumblers with a >= w and a != w
run NonVacuity {
  some disj a, w: Tumbler |
    geq[a, w] and not paddedEqual[a, w]
} for 4 but exactly 2 Tumbler, 5 Int

check WellDefinedSubtraction for 5 but 5 Int
