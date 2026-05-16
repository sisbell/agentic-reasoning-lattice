open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
  all i: Int | (i >= 1 and i =< len) iff one comp[i]
  all i: Int | one comp[i] implies comp[i] >= 0
}

-- Zero-padded component: returns 0 for out-of-range positions
fun zcomp[t: Tumbler, i: Int]: Int {
  (i >= 1 and i =< t.len) implies t.comp[i] else 0
}

-- Divergence: first differing position within shared range, or minLen + 1
fun divergence[a, b: Tumbler]: Int {
  let minLen = (a.len =< b.len implies a.len else b.len) |
  let diffs = {k: Int | k >= 1 and k =< minLen and not (a.comp[k] = b.comp[k])} |
  some diffs implies
    {k: diffs | no k2: diffs | k2 < k}
  else
    plus[minLen, 1]
}

-- Zero-padded divergence: first position where zero-padded values differ
fun zpd[a, b: Tumbler]: Int {
  let maxLen = (a.len >= b.len implies a.len else b.len) |
  let diffs = {k: Int | k >= 1 and k =< maxLen and not (zcomp[a, k] = zcomp[b, k])} |
  some diffs implies
    {k: diffs | no k2: diffs | k2 < k}
  else
    0
}

-- Action point: first position with positive component
fun actionPoint[w: Tumbler]: Int {
  let positives = {i: Int | i >= 1 and i =< w.len and w.comp[i] > 0} |
  {i: positives | no i2: positives | i2 < i}
}

-- Tumbler ordering: a < b
pred tumblerLT[a, b: Tumbler] {
  let k = divergence[a, b] |
  let minLen = (a.len =< b.len implies a.len else b.len) |
  k =< minLen implies a.comp[k] < b.comp[k]
  else a.len < b.len
}

-- TumblerSub: result = m ⊖ s (minuend minus subtrahend)
pred TumblerSub[m, s, result: Tumbler] {
  let maxLen = (m.len >= s.len implies m.len else s.len) |
  let k = zpd[m, s] | {
    result.len = maxLen
    k = 0 implies
      (all i: Int | i >= 1 and i =< maxLen implies result.comp[i] = 0)
    else (
      (all i: Int | (i >= 1 and i < k) implies result.comp[i] = 0)
      and result.comp[k] = minus[zcomp[m, k], zcomp[s, k]]
      and (all i: Int | (i > k and i =< maxLen) implies result.comp[i] = zcomp[m, i])
    )
  }
}

-- TumblerAdd: result = a ⊕ w
pred TumblerAdd[a, w, result: Tumbler] {
  some actionPoint[w]
  let k = actionPoint[w] | {
    k =< a.len
    result.len = w.len
    all i: Int | (i >= 1 and i < k) implies result.comp[i] = a.comp[i]
    result.comp[k] = plus[a.comp[k], w.comp[k]]
    all i: Int | (i > k and i =< w.len) implies result.comp[i] = w.comp[i]
  }
}

-- Structural equality
pred tumblerEq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | i >= 1 and i =< a.len implies a.comp[i] = b.comp[i]
}

-- D2: DisplacementUnique
-- For a < b with divergence(a,b) <= #a and #a <= #b: if a ⊕ w = b then w = b ⊖ a
assert DisplacementUnique {
  all disj a, b, w, bma: Tumbler |
    (tumblerLT[a, b] and divergence[a, b] =< a.len and a.len =< b.len
     and TumblerAdd[a, w, b] and TumblerSub[b, a, bma])
    implies tumblerEq[w, bma]
}

-- Non-vacuity
run NonVacuity {
  some disj a, b, w, bma: Tumbler |
    tumblerLT[a, b] and divergence[a, b] =< a.len and a.len =< b.len
    and TumblerAdd[a, w, b] and TumblerSub[b, a, bma]
} for 5 but exactly 4 Tumbler, 5 Int

check DisplacementUnique for 5 but exactly 4 Tumbler, 5 Int
