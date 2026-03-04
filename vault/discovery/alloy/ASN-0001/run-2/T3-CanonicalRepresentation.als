-- T3 — CanonicalRepresentation
-- Tumblers have canonical (extensional) equality:
-- two tumblers are equal iff they have the same length and
-- identical components at every position.

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

-- Well-formedness: components defined exactly at positions 1..len,
-- all values non-negative, length at least 1.
fact WellFormed {
  all t: Tumbler {
    t.len >= 1
    all i: Int | (i >= 1 and i =< t.len) implies one t.comp[i]
    all i: Int | (i < 1 or i > t.len) implies no t.comp[i]
    all i: Int | some t.comp[i] implies t.comp[i] >= 0
  }
}

-- The canonical representation invariant:
-- distinct tumbler atoms must differ in length or in at least one component.
fact Canonical {
  all disj a, b: Tumbler |
    a.len != b.len or
    (some i: Int | i >= 1 and i =< a.len and a.comp[i] != b.comp[i])
}

-- Component-wise equality predicate
pred componentEqual[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]
}

-- T3: component-wise equality is equivalent to identity
assert CanonicalRepresentation {
  all a, b: Tumbler |
    componentEqual[a, b] iff a = b
}

-- Non-vacuity: the model admits at least two distinct tumblers
run NonVacuity {
  #Tumbler >= 2
} for 4 but 5 Int

check CanonicalRepresentation for 5 but 5 Int
