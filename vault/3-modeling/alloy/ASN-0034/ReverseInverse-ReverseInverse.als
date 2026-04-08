open util/ordering[Pos]

sig Pos {}

sig Tumbler {
  lastPos: one Pos,
  comp: Pos -> lone Int
} {
  all p: Pos | lte[p, lastPos] iff one comp[p]
  all p: Pos | some comp[p] implies comp[p] >= 0
}

fun positions[t: Tumbler]: set Pos {
  {p: Pos | lte[p, t.lastPos]}
}

pred isPositive[t: Tumbler] {
  some p: positions[t] | t.comp[p] > 0
}

pred isActionPoint[t: Tumbler, k: Pos] {
  k in positions[t]
  t.comp[k] > 0
  all p: Pos | (p in positions[t] and lt[p, k]) implies t.comp[p] = 0
}

pred tumblerEq[a, b: Tumbler] {
  a.lastPos = b.lastPos
  all p: positions[a] | a.comp[p] = b.comp[p]
}

-- Lexicographic a >= w (same-length tumblers)
pred geq[a, w: Tumbler] {
  a.lastPos = w.lastPos
  tumblerEq[a, w] or
  (some k: positions[a] |
    a.comp[k] > w.comp[k] and
    (all j: Pos | (j in positions[a] and lt[j, k]) implies
      a.comp[j] = w.comp[j]))
}

-- TumblerAdd: r = a ⊕ w with action point k
-- Pre: w > 0, k = actionPoint(w), k <= #a
-- Post: r_i = a_i (i < k), r_k = a_k + w_k, r_i = w_i (i > k), #r = #w
pred tumblerAdd[a, w, r: Tumbler, k: Pos] {
  isPositive[w]
  isActionPoint[w, k]
  lte[k, a.lastPos]
  r.lastPos = w.lastPos
  all p: positions[r] | {
    lt[p, k] implies r.comp[p] = a.comp[p]
    p = k implies r.comp[p] = plus[a.comp[p], w.comp[p]]
    gt[p, k] implies r.comp[p] = w.comp[p]
  }
}

-- TumblerSub: r = a ⊖ w (same-length)
-- Pre: #a = #w, a >= w
-- Post: divergence-based subtraction, #r = #a
pred tumblerSub[a, w, r: Tumbler] {
  a.lastPos = w.lastPos
  geq[a, w]
  r.lastPos = a.lastPos
  -- Equal: zero tumbler
  tumblerEq[a, w] implies
    (all p: positions[r] | r.comp[p] = 0)
  -- Unequal: first divergence k
  not tumblerEq[a, w] implies
    (some k: positions[a] |
      not (a.comp[k] = w.comp[k]) and
      (all j: Pos | (j in positions[a] and lt[j, k]) implies
        a.comp[j] = w.comp[j]) and
      (all p: positions[r] | {
        lt[p, k] implies r.comp[p] = 0
        p = k implies r.comp[p] = minus[a.comp[p], w.comp[p]]
        gt[p, k] implies r.comp[p] = a.comp[p]
      }))
}

-- ReverseInverse: (a ⊖ w) ⊕ w = a
assert ReverseInverse {
  all a, w, y, r: Tumbler, k: Pos |
    (a.lastPos = k and w.lastPos = k and
     geq[a, w] and isPositive[w] and
     isActionPoint[w, k] and
     (all i: Pos | (i in positions[a] and lt[i, k]) implies
       a.comp[i] = 0) and
     tumblerSub[a, w, y] and
     tumblerAdd[y, w, r, k])
    implies tumblerEq[r, a]
}

check ReverseInverse for 4 but exactly 4 Tumbler, 5 Int

run NonVacuity {
  some disj a, w, y, r: Tumbler, k: Pos |
    a.lastPos = k and w.lastPos = k and
    geq[a, w] and isPositive[w] and
    isActionPoint[w, k] and
    (all i: Pos | (i in positions[a] and lt[i, k]) implies
      a.comp[i] = 0) and
    tumblerSub[a, w, y] and
    tumblerAdd[y, w, r, k]
} for 4 but exactly 4 Tumbler, 5 Int
