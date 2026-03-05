sig Val {}

sig Tumbler {
  comps: seq Val
}

-- Canonical representation: distinct Tumbler atoms must encode distinct sequences.
-- Without this fact, two different atoms could carry identical comps, violating T3.
fact CanonicalRepresentation {
  all a, b: Tumbler | a.comps = b.comps implies a = b
}

-- Component-wise equality: same length and same value at every position.
-- Equivalent to: #a = #b and for all i in 1..#a, a_i = b_i.
pred sameComponents[a, b: Tumbler] {
  a.comps = b.comps
}

-- T3: two tumblers are identical iff their component sequences are identical.
assert T3 {
  all a, b: Tumbler | sameComponents[a, b] iff a = b
}

-- Non-vacuity: two distinct tumblers with differing sequences exist.
run NonVacuous {
  some disj a, b: Tumbler | not sameComponents[a, b]
} for 5 but exactly 2 Tumbler, 3 seq

check T3 for 5 but exactly 2 Tumbler, 3 seq
