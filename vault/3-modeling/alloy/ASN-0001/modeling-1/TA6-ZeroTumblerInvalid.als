-- TA6 — ZeroTumblerInvalid
-- A zero tumbler (every component zero) is not a valid address.
-- Secondary: every zero tumbler is strictly less than every positive tumbler under T1.

sig Tumbler {
  comps: seq Int
}

-- Components are natural numbers (non-negative integers)
fact NaturalComponents {
  all t: Tumbler, i: t.comps.inds | t.comps[i] >= 0
}

-- Zero tumbler: every component is zero (vacuously true for empty sequence)
pred isZero[t: Tumbler] {
  all i: t.comps.inds | t.comps[i] = 0
}

-- Positive tumbler: at least one component is strictly positive
pred isPositive[t: Tumbler] {
  some i: t.comps.inds | t.comps[i] > 0
}

-- A tumbler is a valid address only if it is positive
pred validAddress[t: Tumbler] {
  isPositive[t]
}

-- Simplified T1 ordering for zero-vs-positive case:
-- z <T1 p holds when p has an action point k (first nonzero) and z[k] = 0 < p[k]
pred zeroLessT1[z: Tumbler, p: Tumbler] {
  some k: p.comps.inds | {
    p.comps[k] > 0
    -- k is the first nonzero position in p (action point)
    all j: p.comps.inds | j < k implies p.comps[j] = 0
    -- z's value at k is 0: either k is out of z's range, or z[k] = 0 by isZero
    k not in z.comps.inds or z.comps[k] = 0
  }
}

-- TA6 (primary): every zero tumbler is not a valid address
assert ZeroTumblerInvalid {
  all t: Tumbler | isZero[t] implies not validAddress[t]
}

-- TA6 (corollary): zero and positive are mutually exclusive
assert ZeroPositiveDisjoint {
  no t: Tumbler | isZero[t] and isPositive[t]
}

-- TA6 (secondary): every zero tumbler is strictly less than every positive tumbler
assert ZeroLessThanPositive {
  all z, p: Tumbler |
    (isZero[z] and isPositive[p]) implies zeroLessT1[z, p]
}

-- Non-vacuity: the model admits both zero and positive tumblers
run NonVacuous {
  some z, p: Tumbler | isZero[z] and isPositive[p]
} for 4 but exactly 2 Tumbler, 3 seq, 4 Int

check ZeroTumblerInvalid    for 4 but 3 seq, 4 Int
check ZeroPositiveDisjoint  for 4 but 3 seq, 4 Int
check ZeroLessThanPositive  for 4 but 3 seq, 4 Int
