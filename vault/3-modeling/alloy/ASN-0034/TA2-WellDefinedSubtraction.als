-- TA2: Well-Defined Subtraction (ASN-0034)
-- For tumblers a, w in T with a >= w, a ⊖ w is in T.

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

pred validTumbler[t: Tumbler] {
  t.len >= 1
  all i: Int {
    (i >= 1 and i =< t.len) implies one t.comp[i]
    (i < 1 or i > t.len) implies no t.comp[i]
    some t.comp[i] implies t.comp[i] >= 0
  }
}

fun maxOfTwo[a, b: Int]: one Int {
  (a >= b) => a else b
}

fun minOfTwo[a, b: Int]: one Int {
  (a =< b) => a else b
}

-- Zero-padded component: returns t[i] if in range, else 0
fun zpad[t: Tumbler, i: Int]: one Int {
  (i >= 1 and i =< t.len) => t.comp[i] else 0
}

-- T1 strict ordering: lexicographic with prefix extension
pred tumblerGt[a, w: Tumbler] {
  let m = minOfTwo[a.len, w.len] {
    -- Case (i): first differing component within shared length, a larger
    (some k: Int | k >= 1 and k =< m
      and a.comp[k] > w.comp[k]
      and (all j: Int | (j >= 1 and j < k) implies a.comp[j] = w.comp[j]))
    or
    -- Case (ii): shared components equal, a is longer
    ((all i: Int | (i >= 1 and i =< m) implies a.comp[i] = w.comp[i])
      and a.len > w.len)
  }
}

-- T3 equality: same length and same components
pred tumblerEq[a, w: Tumbler] {
  a.len = w.len
  all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = w.comp[i]
}

pred tumblerGeq[a, w: Tumbler] {
  tumblerEq[a, w] or tumblerGt[a, w]
}

-- Zero-padded divergence: first position where padded sequences differ
pred hasZPD[a, w: Tumbler] {
  some i: Int | i >= 1 and i =< maxOfTwo[a.len, w.len]
    and not (zpad[a, i] = zpad[w, i])
}

fun zpd[a, w: Tumbler]: lone Int {
  let diffs = {i: Int | i >= 1 and i =< maxOfTwo[a.len, w.len]
    and not (zpad[a, i] = zpad[w, i])} |
    {k: diffs | no j: diffs | j < k}
}

-- TumblerSub: r = a ⊖ w
pred TumblerSub[a, w, r: Tumbler] {
  -- Preconditions
  validTumbler[a]
  validTumbler[w]
  tumblerGeq[a, w]

  -- Result length = max(#a, #w)
  r.len = maxOfTwo[a.len, w.len]

  -- Result structure: components defined at 1..r.len
  all i: Int {
    (i >= 1 and i =< r.len) implies one r.comp[i]
    (i < 1 or i > r.len) implies no r.comp[i]
  }

  -- Case 1: no zero-padded divergence -> zero tumbler
  not hasZPD[a, w] implies
    (all i: Int | (i >= 1 and i =< r.len) implies r.comp[i] = 0)

  -- Case 2: divergence at position k
  hasZPD[a, w] implies
    let k = zpd[a, w] {
      -- Pre-divergence: zeros
      all i: Int | (i >= 1 and i < k) implies r.comp[i] = 0
      -- Divergence point: subtract
      r.comp[k] = minus[zpad[a, k], zpad[w, k]]
      -- Tail: copy a's zero-padded values
      all i: Int | (i > k and i =< r.len) implies r.comp[i] = zpad[a, i]
    }
}

-- TA2: subtraction produces a well-defined tumbler
assert WellDefinedSubtraction {
  all a, w, r: Tumbler |
    TumblerSub[a, w, r] implies validTumbler[r]
}

-- Non-vacuity: TumblerSub is satisfiable with distinct tumblers
run NonVacuity {
  some disj a, w, r: Tumbler | TumblerSub[a, w, r]
} for 5 but exactly 3 Tumbler, 4 Int

check WellDefinedSubtraction for 5 but exactly 3 Tumbler, 4 Int
