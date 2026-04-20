-- TA1 (OrderPreservationUnderAddition) — ASN-0034
-- Preconditions: a in T, b in T, w in T, a < b, w > 0, actionPoint(w) <= min(#a, #b)
-- Postcondition: a + w <= b + w

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

-- Well-formed tumbler: length >= 1, components at 1..len are naturals,
-- no components outside that range
pred wellFormed[t: Tumbler] {
  t.len >= 1
  all i: Int {
    (1 =< i and i =< t.len) implies (one t.comp[i] and t.comp[i] >= 0)
    (i < 1 or i > t.len) implies no t.comp[i]
  }
}

-- Overflow guard: bound input values so addition stays within Int range.
-- With 5-bit Int (range -16..15), values 0..7 ensure sums fit.
pred safeRange[t: Tumbler] {
  all i: Int | some t.comp[i] implies t.comp[i] =< 7
}

fact Constraints {
  all t: Tumbler | wellFormed[t] and safeRange[t]
}

-- Positive tumbler: at least one nonzero component
pred isPositive[t: Tumbler] {
  some i: Int | 1 =< i and i =< t.len and t.comp[i] > 0
}

-- Action point: index of first nonzero component
fun actionPoint[t: Tumbler]: Int {
  min[{i: Int | 1 =< i and i =< t.len and t.comp[i] > 0}]
}

-- T1: lexicographic less-than
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

-- Tumbler extensional equality (T3)
pred eqT[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (1 =< i and i =< a.len) implies a.comp[i] = b.comp[i]
}

-- Tumbler less-than-or-equal
pred leT[a, b: Tumbler] {
  ltT[a, b] or eqT[a, b]
}

-- Tumbler addition r = a ⊕ w (constructive definition)
pred tumblerAdd[a, w, r: Tumbler] {
  r.len = w.len
  let k = actionPoint[w] {
    -- Prefix: copy from a
    all i: Int | (1 =< i and i < k) implies r.comp[i] = a.comp[i]
    -- Action point: single-component advance
    r.comp[k] = plus[a.comp[k], w.comp[k]]
    -- Tail: copy from w
    all i: Int | (k < i and i =< w.len) implies r.comp[i] = w.comp[i]
  }
  -- Frame: no components outside 1..r.len
  all i: Int | (i < 1 or i > r.len) implies no r.comp[i]
}

-- TA1: weak order preservation under addition
-- a < b and w > 0 and actionPoint(w) <= min(#a, #b) implies a ⊕ w <= b ⊕ w
assert TA1_OrderPreservationUnderAddition {
  all a, b, w, aw, bw: Tumbler |
    (ltT[a, b] and isPositive[w]
     and actionPoint[w] =< a.len
     and actionPoint[w] =< b.len
     and tumblerAdd[a, w, aw]
     and tumblerAdd[b, w, bw])
    implies leT[aw, bw]
}

-- Non-vacuity: preconditions are satisfiable
run NonVacuity {
  some disj a, b, w, aw, bw: Tumbler |
    ltT[a, b] and isPositive[w]
    and actionPoint[w] =< a.len
    and actionPoint[w] =< b.len
    and tumblerAdd[a, w, aw]
    and tumblerAdd[b, w, bw]
} for 5 but exactly 5 Tumbler, 5 Int

check TA1_OrderPreservationUnderAddition for 6 but 5 Int
