-- TA6-ZeroTumblerInvalid
-- Every zero tumbler is not a valid address; every zero tumbler
-- is strictly less than every positive tumbler under lexicographic order.

open util/ordering[Pos] as po

sig Pos {}

sig Tumbler {
  comp: Pos -> one Int
}

-- Components are non-negative natural numbers
fact NonNegativeComponents {
  all t: Tumbler, p: Pos | t.comp[p] >= 0
}

-- A tumbler is zero when all components are zero
pred isZero[t: Tumbler] {
  all p: Pos | t.comp[p] = 0
}

-- A tumbler is positive when at least one component is nonzero
pred isPositive[t: Tumbler] {
  some p: Pos | t.comp[p] != 0
}

-- A valid address must be positive
pred validAddress[t: Tumbler] {
  isPositive[t]
}

-- Lexicographic strict less-than: at the first position where
-- a and b differ, a has the smaller value
pred lexLT[a, b: Tumbler] {
  some p: Pos {
    a.comp[p] < b.comp[p]
    all q: po/prevs[p] | a.comp[q] = b.comp[q]
  }
}

-- TA6a: Zero tumblers are not valid addresses
assert ZeroNotValidAddress {
  all t: Tumbler | isZero[t] implies not validAddress[t]
}

-- TA6b: Every zero tumbler is less than every positive tumbler
assert ZeroLessThanPositive {
  all z, p: Tumbler |
    (isZero[z] and isPositive[p]) implies lexLT[z, p]
}

-- Non-vacuity: a zero and a positive tumbler coexist with the ordering
run NonVacuity {
  some disj z, p: Tumbler |
    isZero[z] and isPositive[p] and lexLT[z, p]
} for 5 but exactly 2 Tumbler, 4 Pos, 5 Int

check ZeroNotValidAddress for 5 but 4 Pos, 5 Int
check ZeroLessThanPositive for 5 but 4 Pos, 5 Int
