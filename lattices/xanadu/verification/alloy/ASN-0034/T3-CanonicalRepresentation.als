-- T3: CanonicalRepresentation
-- Axiom: Tumbler equality is sequence equality:
-- a = b ⟺ #a = #b ∧ (∀ i : 1 ≤ i ≤ #a : aᵢ = bᵢ)
-- No quotient, normalization, or external identification is imposed on T.

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

-- Well-formedness: tumbler is a valid finite sequence over ℕ
pred wellFormed[t: Tumbler] {
  t.len >= 0
  -- components defined exactly at positions 1..len
  all i: Int | (i >= 1 and i =< t.len) implies one t.comp[i]
  all i: Int | (i < 1 or i > t.len) implies no t.comp[i]
  -- components are natural numbers
  all i: Int | some t.comp[i] implies t.comp[i] >= 0
}

fact AllWellFormed {
  all t: Tumbler | wellFormed[t]
}

-- Two tumblers represent the same sequence
pred sameSequence[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]
}

-- T3 axiom: identical sequences imply identical tumblers
fact T3_CanonicalRepresentation {
  all a, b: Tumbler | sameSequence[a, b] implies a = b
}

-- Full biconditional: identity iff same sequence
assert T3_Biconditional {
  all a, b: Tumbler |
    (a = b) iff sameSequence[a, b]
}

-- Consequence: distinct tumblers must differ in length or some component
assert DistinctTumblersDiffer {
  all a, b: Tumbler | not (a = b) implies
    (not (a.len = b.len) or
     (some i: Int | i >= 1 and i =< a.len and not (a.comp[i] = b.comp[i])))
}

check T3_Biconditional for 5 but 4 Int
check DistinctTumblersDiffer for 5 but 4 Int

-- Non-vacuity: model admits multiple distinct tumblers
run NonVacuity {
  #Tumbler >= 2
} for 4 but 4 Int
