-- T3: CanonicalRepresentation
-- Tumblers have identity determined by their component sequence.
-- (A a, b in T : a1 = b1 /\ ... /\ an = bn /\ #a = #b <=> a = b)

open util/ordering[Idx]

sig Idx {}

sig Val {}

sig Tumbler {
  len: Idx,
  comp: Idx -> lone Val
} {
  -- comp is defined exactly for positions up to len
  all i: Idx | some comp[i] iff lte[i, len]
}

-- Component-wise equality: same length and same value at every position
pred componentEqual[a, b: Tumbler] {
  a.len = b.len
  all i: Idx | a.comp[i] = b.comp[i]
}

-- Axiom: canonical form — no two distinct tumblers share the same components
fact CanonicalForm {
  all disj a, b: Tumbler | not componentEqual[a, b]
}

-- T3: component-wise equality is tumbler identity (biconditional)
assert T3_CanonicalRepresentation {
  all a, b: Tumbler | componentEqual[a, b] iff a = b
}

check T3_CanonicalRepresentation for 5 but exactly 3 Idx, exactly 3 Val

-- Non-vacuity: the model admits distinct tumblers with different components
run NonVacuity {
  some disj a, b: Tumbler | not componentEqual[a, b]
} for 4 but exactly 3 Idx, exactly 3 Val
