-- TA1: WeakOrderPreservation
-- Property (POST): a < b and w > 0 with action point k <= min(#a,#b)
-- implies a+w <= b+w.

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

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

-- Effective value at position i (0 beyond tumbler length)
fun ev[t: Tumbler, i: Int]: Int {
  (some t.comp[i]) implies t.comp[i] else 0
}

-- Positive tumbler: at least one nonzero component
pred positive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] != 0
}

-- Action point: first nonzero position
pred isActionPt[w: Tumbler, k: Int] {
  k >= 1 and k =< w.len
  w.comp[k] != 0
  all j: Int | (j >= 1 and j < k) implies w.comp[j] = 0
}

-- Tumbler addition: r = a ⊕ w with action point k
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPt[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | (i >= 1 and i =< r.len) implies
    ((i < k implies r.comp[i] = a.comp[i]) and
     (i = k implies r.comp[i] = plus[a.comp[k], w.comp[k]]) and
     (i > k implies r.comp[i] = w.comp[i]))
}

-- Strict lexicographic less-than (missing components treated as 0)
pred ltLex[a, b: Tumbler] {
  some p: Int {
    p >= 1 and p =< MAXLEN
    ev[a, p] < ev[b, p]
    all q: Int | (q >= 1 and q < p) implies ev[a, q] = ev[b, q]
  }
}

-- Component-wise equality up to MAXLEN (with zero padding)
pred eqLex[a, b: Tumbler] {
  all p: Int | (p >= 1 and p =< MAXLEN) implies ev[a, p] = ev[b, p]
}

-- Lexicographic less-than-or-equal
pred leLex[a, b: Tumbler] {
  eqLex[a, b] or ltLex[a, b]
}

-- TA1: Weak Order Preservation
-- The overflow guards exclude spurious counterexamples from bounded
-- Int arithmetic; in the mathematical model sums are always non-negative.
assert TA1_WeakOrderPreservation {
  all a, b, w, aw, bw: Tumbler, k: Int |
    (ltLex[a, b] and
     tumblerAdd[a, w, aw, k] and
     tumblerAdd[b, w, bw, k] and
     plus[a.comp[k], w.comp[k]] >= 0 and
     plus[b.comp[k], w.comp[k]] >= 0)
    implies leLex[aw, bw]
}

-- Non-vacuity: the addition-with-ordering scenario is satisfiable
run NonVacuity {
  some disj a, b, w, aw, bw: Tumbler |
    some k: Int |
      ltLex[a, b] and
      tumblerAdd[a, w, aw, k] and
      tumblerAdd[b, w, bw, k] and
      plus[a.comp[k], w.comp[k]] >= 0 and
      plus[b.comp[k], w.comp[k]] >= 0
} for 5 but exactly 5 Tumbler, 5 Int

check TA1_WeakOrderPreservation for 5 but 5 Int
