-- Tumbler Algebra: TA1 weak/strict, TA3 weak/strict, TA4, TA-LC
-- Bounded check for ASN-0034

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fact WF {
  all t: Tumbler {
    t.len >= 1
    t.len =< 3
    all i: Int {
      (i >= 1 and i =< t.len) implies (one t.comp[i] and t.comp[i] >= 0)
      (i < 1 or i > t.len) implies no t.comp[i]
    }
  }
}

fact ComponentBound {
  all t: Tumbler, i: Int | some t.comp[i] implies t.comp[i] =< 7
}

-- Zero-padded component: returns value or 0 beyond length
fun zp[t: Tumbler, i: Int]: Int {
  let c = t.comp[i] | (some c) implies c else 0
}

fun imax[a, b: Int]: Int {
  a >= b implies a else b
}

fun imin[a, b: Int]: Int {
  a =< b implies a else b
}

-- Component-wise tumbler equality
pred tEq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]
}

-- Tumbler strict ordering (T1: lexicographic with prefix rule)
pred tLt[a, b: Tumbler] {
  -- Case (i): first component divergence
  (some k: Int {
    k >= 1 and k =< a.len and k =< b.len
    a.comp[k] < b.comp[k]
    all j: Int | (j >= 1 and j < k) implies a.comp[j] = b.comp[j]
  })
  or
  -- Case (ii): a is proper prefix of b
  (a.len < b.len and
   (all j: Int | (j >= 1 and j =< a.len) implies a.comp[j] = b.comp[j]))
}

pred tLe[a, b: Tumbler] {
  tLt[a, b] or tEq[a, b]
}

pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] > 0
}

-- Action point: first nonzero position in displacement
pred isActionPoint[w: Tumbler, k: Int] {
  k >= 1 and k =< w.len
  w.comp[k] > 0
  all j: Int | (j >= 1 and j < k) implies w.comp[j] = 0
}

-- Divergence (T1 definition): case (i) component mismatch, case (ii) prefix
pred isDivergence[a, b: Tumbler, d: Int] {
  (d >= 1 and d =< a.len and d =< b.len
   and not (a.comp[d] = b.comp[d])
   and (all j: Int | (j >= 1 and j < d) implies a.comp[j] = b.comp[j]))
  or
  (not (a.len = b.len)
   and d = plus[imin[a.len, b.len], 1]
   and (all j: Int | (j >= 1 and j =< imin[a.len, b.len])
            implies a.comp[j] = b.comp[j]))
}

-- Zero-padded divergence for subtraction
pred isZpd[a, w: Tumbler, k: Int] {
  k >= 1 and k =< imax[a.len, w.len]
  not (zp[a, k] = zp[w, k])
  all j: Int | (j >= 1 and j < k) implies zp[a, j] = zp[w, j]
}

-- TumblerAdd: r = a (+) w
pred TumblerAdd[a, w, r: Tumbler] {
  some k: Int {
    isActionPoint[w, k]
    k =< a.len
    r.len = w.len
    all i: Int | (i >= 1 and i =< r.len) implies {
      i < k implies r.comp[i] = a.comp[i]
      i = k implies r.comp[i] = plus[a.comp[i], w.comp[i]]
      i > k implies r.comp[i] = w.comp[i]
    }
  }
}

-- TumblerSub: r = a (-) w
pred TumblerSub[a, w, r: Tumbler] {
  r.len = imax[a.len, w.len]
  (
    (some k: Int {
      isZpd[a, w, k]
      all i: Int | (i >= 1 and i =< r.len) implies {
        i < k implies r.comp[i] = 0
        i = k implies r.comp[i] = minus[zp[a, i], zp[w, i]]
        i > k implies r.comp[i] = zp[a, i]
      }
    })
    or
    ((no k: Int | isZpd[a, w, k]) and
     (all i: Int | (i >= 1 and i =< r.len) implies r.comp[i] = 0))
  )
}

-- TA1 weak: a < b, w > 0, additions well-defined => a(+)w =< b(+)w
assert TA1weak {
  all a, b, w, r1, r2: Tumbler |
    (tLt[a, b] and isPositive[w]
     and TumblerAdd[a, w, r1] and TumblerAdd[b, w, r2])
    implies tLe[r1, r2]
}

-- TA1 strict: additionally k >= divergence(a,b) => a(+)w < b(+)w
assert TA1strict {
  all a, b, w, r1, r2: Tumbler |
    (tLt[a, b] and isPositive[w]
     and TumblerAdd[a, w, r1] and TumblerAdd[b, w, r2]
     and (all k: Int | isActionPoint[w, k] implies
           (some d: Int | isDivergence[a, b, d] and k >= d)))
    implies tLt[r1, r2]
}

-- TA3 weak: a < b, a >= w, b >= w => a(-)w =< b(-)w
assert TA3weak {
  all a, b, w, r1, r2: Tumbler |
    (tLt[a, b] and tLe[w, a] and tLe[w, b]
     and TumblerSub[a, w, r1] and TumblerSub[b, w, r2])
    implies tLe[r1, r2]
}

-- TA3 strict: additionally #a = #b => a(-)w < b(-)w
assert TA3strict {
  all a, b, w, r1, r2: Tumbler |
    (tLt[a, b] and tLe[w, a] and tLe[w, b] and a.len = b.len
     and TumblerSub[a, w, r1] and TumblerSub[b, w, r2])
    implies tLt[r1, r2]
}

-- TA4: (a(+)w) (-) w = a under zero-prefix conditions
assert TA4 {
  all a, w, r1, r2: Tumbler |
    (isPositive[w]
     and (some k: Int {
           isActionPoint[w, k]
           k = a.len
           w.len = k
           all j: Int | (j >= 1 and j < k) implies a.comp[j] = 0
         })
     and TumblerAdd[a, w, r1]
     and TumblerSub[r1, w, r2])
    implies tEq[r2, a]
}

-- TA-LC: a(+)x = a(+)y => x = y
assert TALC {
  all a, x, y, r1, r2: Tumbler |
    (isPositive[x] and isPositive[y]
     and TumblerAdd[a, x, r1] and TumblerAdd[a, y, r2]
     and tEq[r1, r2])
    implies tEq[x, y]
}

-- Non-vacuity
run NonVacuity {
  some a, b, w, r1, r2: Tumbler |
    tLt[a, b] and isPositive[w]
    and TumblerAdd[a, w, r1] and TumblerAdd[b, w, r2]
} for 5 but 5 Int

check TA1weak for 5 but 5 Int
check TA1strict for 5 but 5 Int
check TA3weak for 5 but 5 Int
check TA3strict for 5 but 5 Int
check TA4 for 5 but 5 Int
check TALC for 5 but 5 Int
