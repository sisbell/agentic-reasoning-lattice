open util/integer

-- T0: Carrier Set Definition
-- Axiom: T is the set of all finite sequences over N with length >= 1;
--        N is closed under successor and addition.

sig Tumbler {
  digits: seq Int
}

-- Carrier set axiom: tumblers are non-empty sequences of natural numbers
fact CarrierSetDefinition {
  all t: Tumbler {
    -- n >= 1: every tumbler has at least one digit
    some t.digits
    -- each di in N: every component is a natural number (non-negative)
    all i: Int | some t.digits[i] implies t.digits[i] >= 0
  }
}

-- Structural assertion: no tumbler is the empty sequence
assert LengthAtLeastOne {
  all t: Tumbler | #t.digits >= 1
}

-- Structural assertion: all components are non-negative
assert ComponentsNatural {
  all t: Tumbler | all i: Int | some t.digits[i] implies t.digits[i] >= 0
}

-- Non-vacuity: the axiom admits tumblers of varying lengths
run NonVacuity {
  some disj t1, t2: Tumbler {
    #t1.digits = 1
    #t2.digits >= 2
  }
} for 5 but exactly 2 Tumbler, 4 seq, 5 Int

check LengthAtLeastOne for 5 but 4 seq, 5 Int
check ComponentsNatural for 5 but 4 seq, 5 Int
