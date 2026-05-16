open util/integer

-- Tumbler: finite sequence of natural numbers (length >= 0)
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

pred wellFormed[t: Tumbler] {
  t.len >= 0
  all i: Int | (i >= 1 and i =< t.len) implies one i.(t.comp)
  all i: Int | (i < 1 or i > t.len) implies no i.(t.comp)
  all i: Int | (i >= 1 and i =< t.len) implies t.comp[i] >= 0
}

fact { all t: Tumbler | wellFormed[t] }

-- Zero tumbler: all components are zero (vacuously true for empty tumblers)
pred isZero[t: Tumbler] {
  all i: Int | (i >= 1 and i =< t.len) implies t.comp[i] = 0
}

-- Has at least one positive component
pred hasPositiveComponent[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] > 0
}

-- Valid address per T4: first component positive
pred validAddress[t: Tumbler] {
  t.len >= 1
  t.comp[1] > 0
}

-- T1 ordering: lexicographic with proper-prefix extension
pred lt[a, b: Tumbler] {
  -- Case (i): first difference within shared length, a component smaller
  (some d: Int |
    d >= 1 and d =< a.len and d =< b.len and
    a.comp[d] < b.comp[d] and
    (all i: Int | (i >= 1 and i < d) implies a.comp[i] = b.comp[i]))
  or
  -- Case (ii): a is proper prefix of b
  (a.len < b.len and
    (all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]))
}

-- TA6 Conjunct 1: no zero tumbler is a valid address
assert ZeroNotValidAddress {
  all t: Tumbler | isZero[t] implies not validAddress[t]
}

-- TA6 Conjunct 2: every zero tumbler < every positive tumbler
assert ZeroLessThanPositive {
  all s, t: Tumbler |
    (isZero[s] and hasPositiveComponent[t]) implies lt[s, t]
}

-- Non-vacuity: a zero and a positive tumbler exist with the zero less
run NonVacuity {
  some s, t: Tumbler |
    isZero[s] and hasPositiveComponent[t] and lt[s, t]
} for 4 but 5 Int

check ZeroNotValidAddress for 5 but 5 Int
check ZeroLessThanPositive for 5 but 5 Int
