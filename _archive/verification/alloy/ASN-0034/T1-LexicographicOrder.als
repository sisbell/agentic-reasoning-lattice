sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fact WellFormed {
  all t: Tumbler {
    t.len >= 1
    t.len =< 6
    all pos: Int {
      (pos >= 1 and pos =< t.len) implies one t.comp[pos]
      (pos < 1 or pos > t.len) implies no t.comp[pos]
    }
    all pos: Int | some t.comp[pos] implies t.comp[pos] >= 0
  }
}

-- T3: distinct atoms must have distinct sequences
fact T3_CanonicalRepresentation {
  all disj a, b: Tumbler |
    not (a.len = b.len) or
    (some i: Int | i >= 1 and i =< a.len and not (a.comp[i] = b.comp[i]))
}

-- T1: lexicographic less-than
pred ltT[a, b: Tumbler] {
  some k: Int {
    k >= 1
    all i: Int | (i >= 1 and i < k) implies a.comp[i] = b.comp[i]
    (k =< a.len and k =< b.len and a.comp[k] < b.comp[k])
    or
    (k = plus[a.len, 1] and k =< b.len)
  }
}

-- (a) Irreflexivity: not (a < a)
assert Irreflexivity {
  all a: Tumbler | not ltT[a, a]
}

-- (b) Trichotomy: exactly one of a < b, a = b, b < a
assert Trichotomy {
  all a, b: Tumbler |
    (ltT[a, b] and not (a = b) and not ltT[b, a]) or
    (not ltT[a, b] and a = b and not ltT[b, a]) or
    (not ltT[a, b] and not (a = b) and ltT[b, a])
}

-- (c) Transitivity: a < b and b < c implies a < c
assert Transitivity {
  all a, b, c: Tumbler |
    (ltT[a, b] and ltT[b, c]) implies ltT[a, c]
}

run NonVacuity {
  some a, b: Tumbler | ltT[a, b]
} for 3 but exactly 2 Tumbler, 4 Int

check Irreflexivity for 4 but 4 Int
check Trichotomy for 4 but 4 Int
check Transitivity for 4 but 4 Int
