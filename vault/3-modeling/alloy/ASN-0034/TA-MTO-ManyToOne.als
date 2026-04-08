-- TA-MTO (ManyToOne)
-- Property: a ⊕ w = b ⊕ w ⟺ (A i : 1 ≤ i ≤ actionPoint(w) : a_i = b_i)
--
-- Two tumblers produce the same result under a displacement if and only if
-- they agree on every component up to and including the action point.

sig Tumbler {
  len: Int,
  c1: Int,
  c2: Int,
  c3: Int
}

-- Components are non-negative natural numbers
fact NonNegComponents {
  all t: Tumbler | t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0
}

-- Length is 1, 2, or 3 (bounded model)
fact ValidLength {
  all t: Tumbler | t.len >= 1 and t.len =< 3
}

-- Components beyond the tumbler's length are zero
fact ZeroPadding {
  all t: Tumbler |
    (t.len < 2 implies t.c2 = 0) and
    (t.len < 3 implies t.c3 = 0)
}

-- Bound values to avoid integer overflow (5 Int = -16..15, max sum 7+7=14)
fact BoundedValues {
  all t: Tumbler | t.c1 =< 7 and t.c2 =< 7 and t.c3 =< 7
}

-- A positive tumbler has at least one component > 0
pred positive[t: Tumbler] {
  t.c1 > 0 or t.c2 > 0 or t.c3 > 0
}

-- Action point: first non-zero position (positions before it are zero)
fun actionPoint[w: Tumbler]: Int {
  w.c1 > 0 => 1 else w.c2 > 0 => 2 else w.c3 > 0 => 3 else 0
}

-- Component-wise tumbler equality
pred tumblerEq[a, b: Tumbler] {
  a.len = b.len and a.c1 = b.c1 and a.c2 = b.c2 and a.c3 = b.c3
}

-- TumblerAdd: result = a ⊕ w
-- Preconditions: w > 0, actionPoint(w) ≤ #a
-- Definition: r_i = a_i if i < k; r_k = a_k + w_k; r_i = w_i if i > k
-- Postcondition: #(a ⊕ w) = #w
pred tumblerAdd[a, w, result: Tumbler] {
  positive[w]
  actionPoint[w] =< a.len
  result.len = w.len
  let k = actionPoint[w] |
    (k = 1 implies (
      result.c1 = plus[a.c1, w.c1] and
      result.c2 = w.c2 and
      result.c3 = w.c3
    )) and
    (k = 2 implies (
      result.c1 = a.c1 and
      result.c2 = plus[a.c2, w.c2] and
      result.c3 = w.c3
    )) and
    (k = 3 implies (
      result.c1 = a.c1 and
      result.c2 = a.c2 and
      result.c3 = plus[a.c3, w.c3]
    ))
}

-- Agreement on components 1..k
pred agreeUpTo[a, b: Tumbler, k: Int] {
  (k >= 1 implies a.c1 = b.c1) and
  (k >= 2 implies a.c2 = b.c2) and
  (k >= 3 implies a.c3 = b.c3)
}

-- TA-MTO Forward: agreement on 1..k implies equal results
assert MTO_Forward {
  all a, b, w, ra, rb: Tumbler |
    (tumblerAdd[a, w, ra] and tumblerAdd[b, w, rb] and
     agreeUpTo[a, b, actionPoint[w]])
    implies tumblerEq[ra, rb]
}

-- TA-MTO Converse: equal results implies agreement on 1..k
assert MTO_Converse {
  all a, b, w, ra, rb: Tumbler |
    (tumblerAdd[a, w, ra] and tumblerAdd[b, w, rb] and
     tumblerEq[ra, rb])
    implies agreeUpTo[a, b, actionPoint[w]]
}

-- TA-MTO Biconditional: the full iff from the formal contract
assert MTO_Biconditional {
  all a, b, w, ra, rb: Tumbler |
    (tumblerAdd[a, w, ra] and tumblerAdd[b, w, rb])
    implies
    (tumblerEq[ra, rb] iff agreeUpTo[a, b, actionPoint[w]])
}

-- Non-vacuity: two distinct tumblers that produce the same result
run NonVacuity {
  some disj a, b, w, ra, rb: Tumbler |
    tumblerAdd[a, w, ra] and tumblerAdd[b, w, rb] and
    not tumblerEq[a, b] and
    tumblerEq[ra, rb]
} for 5 but exactly 5 Tumbler, 5 Int

check MTO_Forward for 5 but exactly 5 Tumbler, 5 Int
check MTO_Converse for 5 but exactly 5 Tumbler, 5 Int
check MTO_Biconditional for 5 but exactly 5 Tumbler, 5 Int
