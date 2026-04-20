open util/integer

-- Tumblers: variable-length sequences of positive integers
sig Tumbler {
  comp: Int -> lone Int,
  len: Int
}

-- Well-formedness: components defined exactly at positions 1..len, all positive
pred wellFormed[t: Tumbler] {
  t.len >= 1
  all p: Int | (p >= 1 and p =< t.len) implies one t.comp[p]
  all p: Int | (p < 1 or p > t.len) implies no t.comp[p]
  all p: Int | some t.comp[p] implies t.comp[p] >= 1
}

-- Sibling allocation: inc(t, 0) per TA5(c) — same length, increment last
pred incSibling[t, result: Tumbler] {
  result.len = t.len
  all p: Int | (p >= 1 and p < t.len) implies result.comp[p] = t.comp[p]
  result.comp[t.len] = plus[t.comp[t.len], 1]
}

-- Child allocation: inc(t, 1) per TA5(b,d) — copies parent, appends child
pred incChild[t, result: Tumbler] {
  result.len = plus[t.len, 1]
  all p: Int | (p >= 1 and p =< t.len) implies result.comp[p] = t.comp[p]
  result.comp[plus[t.len, 1]] = 1
}

-- Proper prefix: a is strictly shorter and agrees on all of a's positions
pred isProperPrefix[a, b: Tumbler] {
  a.len < b.len
  all p: Int | (p >= 1 and p =< a.len) implies a.comp[p] = b.comp[p]
}

-- Scenario: t1 = inc(t0, 0) then t2 = inc(t1, 1)
-- Relaxes the k=0 restriction by allowing a child step after a sibling step
pred setup[t0, t1, t2: Tumbler] {
  wellFormed[t0]
  wellFormed[t1]
  wellFormed[t2]
  incSibling[t0, t1]
  incChild[t1, t2]
}

-- Assert: prefix nesting does NOT occur among produced addresses
-- Expect COUNTEREXAMPLE: t1 IS a proper prefix of t2, violating T10 precondition
assert AllocatorDisciplineNecessity {
  all t0, t1, t2: Tumbler |
    setup[t0, t1, t2] implies not isProperPrefix[t1, t2]
}

-- Non-vacuity: the setup is satisfiable
run NonVacuity {
  some disj t0, t1, t2: Tumbler |
    setup[t0, t1, t2]
} for 5 but exactly 3 Tumbler, 5 Int

check AllocatorDisciplineNecessity for 5 but exactly 3 Tumbler, 5 Int
