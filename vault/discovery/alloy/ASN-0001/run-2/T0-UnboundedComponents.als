open util/integer

-- Index positions (tumblers up to length 3)
abstract sig Idx {}
one sig I1, I2, I3 extends Idx {}

sig Tumbler {
  comp: Idx -> lone Int
}

-- Positions of a tumbler: indices with defined components
fun positions[t: Tumbler]: set Idx {
  {i: Idx | some t.comp[i]}
}

-- Components are non-negative
fact NonNeg {
  all t: Tumbler, i: positions[t] | t.comp[i] >= 0
}

-- Every tumbler has at least one position
fact NonEmpty {
  all t: Tumbler | some positions[t]
}

-- Positions form a contiguous prefix from I1
fact Contiguous {
  all t: Tumbler {
    I3 in positions[t] implies I2 in positions[t]
    I2 in positions[t] implies I1 in positions[t]
  }
}

-- Two tumblers agree except at position i
pred agreesExceptAt[t, t2: Tumbler, i: Idx] {
  positions[t] = positions[t2]
  i in positions[t]
  all j: positions[t] - i | t.comp[j] = t2.comp[j]
}

-- T0 — UnboundedComponents:
-- For every tumbler and position, there exists another tumbler
-- with a strictly larger component value at that position.
-- In the infinite mathematical model this always holds because
-- natural numbers are unbounded. In Alloy's finite scope a
-- counterexample is expected at the Int boundary.
assert UnboundedComponents {
  all t: Tumbler, i: positions[t] |
    some t2: Tumbler |
      agreesExceptAt[t, t2, i] and t2.comp[i] > t.comp[i]
}

check UnboundedComponents for 5 but 5 Int

-- Non-vacuity: satisfiable model with multi-component tumblers
run NonVacuity {
  some t: Tumbler | #positions[t] >= 2
} for 3 but 4 Int
