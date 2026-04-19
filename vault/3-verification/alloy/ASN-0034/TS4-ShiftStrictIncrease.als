open util/ordering[Pos]

-- Ordered positions for tumbler indexing
sig Pos {}

-- Tumbler: sequence of non-negative integers indexed by position
sig Tumbler {
  comp: Pos -> lone Int
}

-- Bound component values to prevent integer overflow
-- With 5 Int (range -16..15), components in 0..7 keep sums in range
fact IntBounds {
  all t: Tumbler, p: Pos | some t.comp[p] implies
    t.comp[p] >= 0 and t.comp[p] =< 7
}

-- Domain: set of positions with defined components
fun dom[t: Tumbler]: set Pos {
  {p: Pos | some t.comp[p]}
}

-- Well-formed tumbler: non-empty contiguous prefix, non-negative components
pred wf[t: Tumbler] {
  some dom[t]
  all p: Pos | p in dom[t] implies t.comp[p] >= 0
  all p: Pos | p in dom[t] implies (p = first or prev[p] in dom[t])
}

-- Length of a tumbler
fun len[t: Tumbler]: Int {
  #dom[t]
}

-- Last defined position
fun lastPos[t: Tumbler]: lone Pos {
  {p: dom[t] | no q: dom[t] | gt[q, p]}
}

-- Lexicographic strict less-than
pred tLt[a, b: Tumbler] {
  -- Prefix case: a is a proper prefix of b
  (dom[a] in dom[b] and
   (all p: dom[a] | a.comp[p] = b.comp[p]) and
   #dom[b] > #dom[a])
  or
  -- Divergence case: first differing shared position has a < b
  (some p: dom[a] & dom[b] |
    (all q: Pos | lt[q, p] implies
      (q in dom[a] implies (q in dom[b] and a.comp[q] = b.comp[q])))
    and a.comp[p] < b.comp[p])
}

-- Strict greater-than
pred tGt[a, b: Tumbler] {
  tLt[b, a]
}

-- Action point: first non-zero position
fun actionPt[w: Tumbler]: lone Pos {
  {p: dom[w] | w.comp[p] > 0 and
    (all q: dom[w] | lt[q, p] implies w.comp[q] = 0)}
}

-- Ordinal displacement delta(n, m): [0, ..., 0, n] of length m
pred isOrdDisp[d: Tumbler, n: Int, m: Int] {
  wf[d]
  len[d] = m
  d.comp[lastPos[d]] = n
  all p: dom[d] | not (p = lastPos[d]) implies d.comp[p] = 0
}

-- Tumbler addition: r = a oplus w
-- k = actionPoint(w); r_i = a_i for i < k; r_k = a_k + w_k; r_i = w_i for i > k
-- Precondition: actionPoint(w) in dom(a). Result length = length of w.
pred isTumblerAdd[r, a, w: Tumbler] {
  some actionPt[w]
  let k = actionPt[w] {
    k in dom[a]
    dom[r] = dom[w]
    all p: dom[r] {
      lt[p, k] implies r.comp[p] = a.comp[p]
      p = k implies r.comp[p] = plus[a.comp[k], w.comp[k]]
      gt[p, k] implies r.comp[p] = w.comp[p]
    }
  }
}

-- Shift: shift(v, n) = v oplus delta(n, len(v))
pred isShift[result, v: Tumbler, n: Int] {
  some d: Tumbler |
    isOrdDisp[d, n, len[v]] and isTumblerAdd[result, v, d]
}

-- TS4: ShiftStrictIncrease
-- For all v in T, n >= 1, #v = m: shift(v, n) > v
assert ShiftStrictIncrease {
  all v, result: Tumbler, n: Int |
    (wf[v] and n >= 1 and isShift[result, v, n])
      implies tGt[result, v]
}

-- Non-vacuity: find a valid shift instance
run NonVacuity {
  some v, result: Tumbler, n: Int |
    wf[v] and n >= 1 and isShift[result, v, n]
} for 4 but exactly 2 Pos, 5 Int

check ShiftStrictIncrease for 4 but exactly 2 Pos, 5 Int
