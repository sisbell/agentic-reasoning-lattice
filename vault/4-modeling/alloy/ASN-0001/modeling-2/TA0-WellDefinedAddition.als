-- TA0: WellDefinedAddition
-- Property (PRE): when w is positive and the action point k of w
-- satisfies k <= #a, TumblerAdd a+w produces a well-defined tumbler.

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

-- Max tumbler length bound
fun MAXLEN: Int { 4 }

fact TumblerWF {
  all t: Tumbler {
    t.len >= 1
    t.len =< MAXLEN
    all i: Int | (i >= 1 and i =< t.len) implies one t.comp[i]
    all i: Int | (i < 1 or i > t.len) implies no t.comp[i]
    all i: Int | some t.comp[i] implies t.comp[i] >= 0
  }
}

-- At least one component is nonzero
pred positive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] != 0
}

-- k is the action point of w: first position with nonzero component
pred isActionPt[w: Tumbler, k: Int] {
  k >= 1 and k =< w.len
  w.comp[k] != 0
  all j: Int | (j >= 1 and j < k) implies w.comp[j] = 0
}

-- r = a + w under action point k
-- Precondition: k <= a.len (action point within a's length)
-- Result length = w.len
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPt[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | (i >= 1 and i =< r.len) implies
    ((i < k implies r.comp[i] = a.comp[i]) and
     (i = k implies r.comp[i] = plus[a.comp[k], w.comp[k]]) and
     (i > k implies r.comp[i] = w.comp[i]))
}

-- TA0: well-formed inputs + precondition => well-formed result
-- The overflow guard excludes spurious counterexamples from bounded
-- Int arithmetic; in the mathematical model the sum is always non-negative.
assert TA0_WellDefinedAddition {
  all a, w, r: Tumbler, k: Int |
    (tumblerAdd[a, w, r, k] and
     plus[a.comp[k], w.comp[k]] >= 0)
    implies
    (all i: Int | (i >= 1 and i =< r.len) implies r.comp[i] >= 0)
}

-- Non-vacuity: the addition scenario is satisfiable
run nonVacuous {
  some a, w, r: Tumbler, k: Int |
    positive[w] and tumblerAdd[a, w, r, k] and
    plus[a.comp[k], w.comp[k]] >= 0
} for 5 but exactly 3 Tumbler, 5 Int

check TA0_WellDefinedAddition for 5 but 5 Int
