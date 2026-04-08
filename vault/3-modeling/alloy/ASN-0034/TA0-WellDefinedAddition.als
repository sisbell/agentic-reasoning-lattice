-- TA0-WellDefinedAddition
-- Preconditions: a in T, w in T, w > 0, actionPoint(w) <= #a
-- Postconditions: a + w in T, #(a + w) = #w

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

-- Positive tumbler: at least one nonzero component
pred isPositive[t: Tumbler] {
  some i: Int | 1 =< i and i =< t.len and t.comp[i] > 0
}

-- Action point: index of first nonzero component
fun actionPoint[t: Tumbler]: Int {
  min[{i: Int | 1 =< i and i =< t.len and t.comp[i] > 0}]
}

-- Tumbler addition r = a + w (constructive definition)
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

-- Overflow guard: bound input values so addition stays within Int range.
-- With 5-bit Int (range -16..15), values 0..7 ensure sums fit.
pred safeRange[t: Tumbler] {
  all i: Int | some t.comp[i] implies t.comp[i] =< 7
}

-- Postcondition 1: result is a well-formed tumbler
assert WellDefinedAddition {
  all a, w, r: Tumbler |
    (wellFormed[a] and wellFormed[w] and isPositive[w]
     and safeRange[a] and safeRange[w]
     and actionPoint[w] =< a.len
     and tumblerAdd[a, w, r])
    implies
    wellFormed[r]
}

-- Postcondition 2: result length equals displacement length
assert ResultLength {
  all a, w, r: Tumbler |
    (wellFormed[a] and wellFormed[w] and isPositive[w]
     and actionPoint[w] =< a.len
     and tumblerAdd[a, w, r])
    implies
    r.len = w.len
}

-- Non-vacuity: a valid addition exists
run NonVacuity {
  some disj a, w, r: Tumbler |
    wellFormed[a] and wellFormed[w] and isPositive[w]
    and safeRange[a] and safeRange[w]
    and actionPoint[w] =< a.len
    and tumblerAdd[a, w, r]
} for 5 but exactly 3 Tumbler, 5 Int

check WellDefinedAddition for 5 but exactly 3 Tumbler, 5 Int
check ResultLength for 5 but exactly 3 Tumbler, 5 Int
