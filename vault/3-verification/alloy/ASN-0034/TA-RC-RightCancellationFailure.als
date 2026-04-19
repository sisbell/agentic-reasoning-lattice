-- TA-RC (RightCancellationFailure)
-- Axiom: ∃ a, b, w ∈ T : w > 0 ∧ actionPoint(w) ≤ #a ∧ actionPoint(w) ≤ #b
--        ∧ a ≠ b ∧ a ⊕ w = b ⊕ w
--
-- Right cancellation fails because TumblerAdd's tail-copy rule discards
-- start components after the action point, replacing them with the
-- displacement's tail.

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

-- A positive tumbler has at least one component > 0
pred positive[t: Tumbler] {
  t.c1 > 0 or t.c2 > 0 or t.c3 > 0
}

-- Action point: first position k where w_k > 0
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

-- Assert right cancellation: if a ⊕ w = b ⊕ w then a = b
-- A counterexample demonstrates the axiom (right cancellation failure)
assert RightCancellation {
  all a, b, w, ra, rb: Tumbler |
    (tumblerAdd[a, w, ra] and tumblerAdd[b, w, rb] and tumblerEq[ra, rb])
    implies tumblerEq[a, b]
}

-- Non-vacuity: the failure scenario is satisfiable
run NonVacuity {
  some a, b, w, ra, rb: Tumbler |
    not tumblerEq[a, b] and
    tumblerAdd[a, w, ra] and
    tumblerAdd[b, w, rb] and
    tumblerEq[ra, rb]
} for 5 but 5 Int

check RightCancellation for 5 but 5 Int
