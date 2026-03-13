open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
  -- components exist exactly at positions 1..len
  all i: Int | (i >= 1 and i =< len) implies one comp[i]
  all i: Int | (i < 1 or i > len) implies no comp[i]
  -- components are non-negative
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- Zero tumbler: every component is zero
pred isZero[t: Tumbler] {
  all i: Int | (i >= 1 and i =< t.len) implies t.comp[i] = 0
}

-- Positive tumbler: at least one component is nonzero
pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] > 0
}

-- T1 lexicographic ordering with prefix rule: a < b
pred lessThan[a, b: Tumbler] {
  -- Case 1: component divergence within shared length
  (some k: Int {
    k >= 1
    k =< a.len
    k =< b.len
    not (a.comp[k] = b.comp[k])
    all j: Int | (j >= 1 and j < k) implies a.comp[j] = b.comp[j]
    a.comp[k] < b.comp[k]
  })
  or
  -- Case 2: a is a proper prefix of b
  (a.len < b.len and
    all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i])
}

-- A valid address must be positive
pred validAddress[t: Tumbler] {
  isPositive[t]
}

-- TA6 Part 1: No zero tumbler is a valid address
assert ZeroNotValidAddress {
  all t: Tumbler | isZero[t] implies not validAddress[t]
}

-- TA6 Part 2: Every zero tumbler is less than every positive tumbler
assert ZeroLessThanPositive {
  all s, t: Tumbler |
    (isZero[s] and isPositive[t]) implies lessThan[s, t]
}

-- Non-vacuity: find a zero tumbler less than a positive one
run NonVacuity {
  some disj s, t: Tumbler |
    isZero[s] and isPositive[t] and lessThan[s, t]
} for 4 but exactly 2 Tumbler, 5 Int

check ZeroNotValidAddress for 5 but 5 Int
check ZeroLessThanPositive for 5 but 5 Int
