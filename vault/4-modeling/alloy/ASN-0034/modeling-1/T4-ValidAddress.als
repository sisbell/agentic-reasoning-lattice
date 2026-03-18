-- T4-ValidAddress.als
-- Valid address invariant for tumbler addresses.
-- At most 3 zero separators; no adjacent zeros, no leading/trailing zero.

open util/integer

sig Tumbler {
  components: seq Int
} {
  all i: Int | (i >= 0 and i < #components) implies components[i] >= 0
  some components
}

fun zeros[t: Tumbler]: Int {
  #{i: Int | i >= 0 and i < #(t.components) and (t.components)[i] = 0}
}

fun tLen[t: Tumbler]: Int {
  #(t.components)
}

-- T4 valid address: at most 3 separating zeros, no adjacent zeros,
-- no leading zero, no trailing zero
pred validAddress[t: Tumbler] {
  zeros[t] =< 3
  (t.components)[0] != 0
  (t.components)[minus[tLen[t], 1]] != 0
  no i: Int |
    i >= 0 and i < tLen[t] and
    (t.components)[i] = 0 and
    plus[i, 1] < tLen[t] and
    (t.components)[plus[i, 1]] = 0
}

-- Address level by zero count
pred isNodeAddr[t: Tumbler]    { validAddress[t] and zeros[t] = 0 }
pred isUserAddr[t: Tumbler]    { validAddress[t] and zeros[t] = 1 }
pred isDocAddr[t: Tumbler]     { validAddress[t] and zeros[t] = 2 }
pred isElementAddr[t: Tumbler] { validAddress[t] and zeros[t] = 3 }

-- Valid address has first component positive
assert ValidImpliesPositive {
  all t: Tumbler |
    validAddress[t] implies (t.components)[0] > 0
}

-- Every non-separator component is strictly positive
assert NonSeparatorsPositive {
  all t: Tumbler | validAddress[t] implies
    all i: Int | (i >= 0 and i < tLen[t] and (t.components)[i] != 0)
      implies (t.components)[i] > 0
}

-- Node address: every component is positive (no zeros)
assert NodeAllPositive {
  all t: Tumbler | isNodeAddr[t] implies
    all i: Int | (i >= 0 and i < tLen[t]) implies (t.components)[i] > 0
}

-- Minimum lengths: user >= 3, document >= 5, element >= 7
assert UserMinLen {
  all t: Tumbler | isUserAddr[t] implies tLen[t] >= 3
}

assert DocMinLen {
  all t: Tumbler | isDocAddr[t] implies tLen[t] >= 5
}

assert ElementMinLen {
  all t: Tumbler | isElementAddr[t] implies tLen[t] >= 7
}

-- Non-vacuity: find instances at each address level
run FindNode {
  some t: Tumbler | isNodeAddr[t]
} for 4 but exactly 1 Tumbler, 5 Int, 7 seq

run FindUser {
  some t: Tumbler | isUserAddr[t]
} for 4 but exactly 1 Tumbler, 5 Int, 7 seq

run FindDoc {
  some t: Tumbler | isDocAddr[t]
} for 4 but exactly 1 Tumbler, 5 Int, 7 seq

run FindElement {
  some t: Tumbler | isElementAddr[t]
} for 4 but exactly 1 Tumbler, 5 Int, 7 seq

check ValidImpliesPositive for 5 but exactly 1 Tumbler, 5 Int, 7 seq
check NonSeparatorsPositive for 5 but exactly 1 Tumbler, 5 Int, 7 seq
check NodeAllPositive for 5 but exactly 1 Tumbler, 5 Int, 7 seq
check UserMinLen for 5 but exactly 1 Tumbler, 5 Int, 7 seq
check DocMinLen for 5 but exactly 1 Tumbler, 5 Int, 7 seq
check ElementMinLen for 5 but exactly 1 Tumbler, 5 Int, 7 seq
