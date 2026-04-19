-- TA3: Order Preservation Under Subtraction (Weak) — ASN-0034
-- Preconditions: a, b, w in T, a < b, a >= w, b >= w
-- Postcondition: a ⊖ w <= b ⊖ w

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

pred wellFormed[t: Tumbler] {
  t.len >= 1
  all i: Int {
    (1 =< i and i =< t.len) implies (one t.comp[i] and t.comp[i] >= 0)
    (i < 1 or i > t.len) implies no t.comp[i]
  }
}

-- Bound component values so arithmetic stays within Int range.
-- With 4-bit Int (range -8..7), values 0..6 are safe.
pred safeRange[t: Tumbler] {
  all i: Int | some t.comp[i] implies t.comp[i] =< 6
  t.len =< 4
}

fact Constraints {
  all t: Tumbler | wellFormed[t] and safeRange[t]
}

fun maxOfTwo[a, b: Int]: one Int {
  (a >= b) => a else b
}

-- Zero-padded component: t[i] if in range, else 0
fun zpad[t: Tumbler, i: Int]: one Int {
  (i >= 1 and i =< t.len) => t.comp[i] else 0
}

-- T1 strict ordering: lexicographic with prefix extension
pred ltT[a, b: Tumbler] {
  some k: Int {
    k >= 1
    all i: Int | (i >= 1 and i < k) implies a.comp[i] = b.comp[i]
    -- Case (i): component divergence within shared range
    (k =< a.len and k =< b.len and a.comp[k] < b.comp[k])
    or
    -- Case (ii): a is proper prefix of b
    (k = plus[a.len, 1] and k =< b.len)
  }
}

-- Extensional equality (T3)
pred eqT[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (1 =< i and i =< a.len) implies a.comp[i] = b.comp[i]
}

pred leT[a, b: Tumbler] {
  ltT[a, b] or eqT[a, b]
}

pred geT[a, b: Tumbler] {
  eqT[a, b] or ltT[b, a]
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
  geT[a, w]

  -- Result length = max(#a, #w)
  r.len = maxOfTwo[a.len, w.len]

  -- Result components defined at 1..r.len
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

-- TA3: a < b and a >= w and b >= w implies a ⊖ w <= b ⊖ w
assert TA3_OrderPreservationUnderSubtractionWeak {
  all a, b, w, ra, rb: Tumbler |
    (ltT[a, b] and geT[a, w] and geT[b, w]
     and TumblerSub[a, w, ra] and TumblerSub[b, w, rb])
    implies leT[ra, rb]
}

-- Non-vacuity: preconditions are satisfiable
run NonVacuity {
  some disj a, b, w, ra, rb: Tumbler |
    ltT[a, b] and geT[a, w] and geT[b, w]
    and TumblerSub[a, w, ra] and TumblerSub[b, w, rb]
} for 5 but exactly 5 Tumbler, 4 Int

check TA3_OrderPreservationUnderSubtractionWeak for 5 but exactly 5 Tumbler, 4 Int
