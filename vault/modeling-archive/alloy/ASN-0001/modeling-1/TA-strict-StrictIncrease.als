open util/integer

-- A Tumbler is a finite sequence of non-negative integers, 1-indexed.
sig Tumbler {
  comp : Int -> lone Int,
  tlen : Int
} {
  tlen >= 1
  tlen =< 3
  all i : Int | (some comp[i]) iff (i >= 1 and i =< tlen)
  all i : Int, v : Int | comp[i] = v implies (v >= 0 and v =< 6)
}

-- A tumbler is positive iff at least one component is nonzero.
pred pos[t : Tumbler] {
  some i : Int | i >= 1 and i =< t.tlen and not (t.comp[i] = 0)
}

-- Action point: first nonzero 1-indexed position. Requires pos[t].
fun actionPt[t : Tumbler] : Int {
  min[{ i : Int | i >= 1 and i =< t.tlen and not (t.comp[i] = 0) }]
}

-- TumblerAdd: r = a ⊕ w.
-- Precondition (from TA0): w is positive and actionPt[w] =< a.tlen.
pred tumblerAdd[a, w, r : Tumbler] {
  pos[w]
  let k = actionPt[w] {
    k =< a.tlen
    r.tlen = w.tlen
    -- Prefix: copy from a
    all i : Int | (i >= 1 and i < k) implies r.comp[i] = a.comp[i]
    -- Action point: single-component advance
    r.comp[k] = plus[a.comp[k], w.comp[k]]
    -- Tail: copy from w (not from a)
    all i : Int | (i > k and i =< w.tlen) implies r.comp[i] = w.comp[i]
  }
}

-- Lexicographic strict order: r > a, treating missing positions as 0.
-- Witness d is the first position where r exceeds a.
pred gtLex[r, a : Tumbler] {
  some d : Int | {
    d >= 1
    -- Equal prefix with extension-by-zero for shorter tumblers
    all i : Int | (i >= 1 and i < d) implies {
      (i =< r.tlen and i =< a.tlen) implies r.comp[i] = a.comp[i]
      (i =< r.tlen and i > a.tlen) implies r.comp[i] = 0
      (i > r.tlen and i =< a.tlen) implies a.comp[i] = 0
    }
    -- r is strictly greater at d
    d =< r.tlen
    (d =< a.tlen implies r.comp[d] > a.comp[d])
    (d > a.tlen implies r.comp[d] > 0)
  }
}

-- TA-strict (StrictIncrease): for every well-defined addition, a ⊕ w > a.
assert StrictIncrease {
  all a, w, r : Tumbler | tumblerAdd[a, w, r] implies gtLex[r, a]
}

-- Non-vacuity: confirm the model admits at least one valid addition instance.
run NonVacuous {
  some a, w, r : Tumbler | tumblerAdd[a, w, r]
} for 4 but exactly 3 Tumbler, 5 Int

check StrictIncrease for 4 but exactly 3 Tumbler, 5 Int
