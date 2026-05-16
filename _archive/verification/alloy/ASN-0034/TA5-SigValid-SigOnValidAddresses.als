-- TA5-SigValid (SigOnValidAddresses)
-- For every valid address t satisfying T4, sig(t) = #t.
-- ASN-0034

-- Tumbler: sequence of non-negative integers indexed 1..len
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  -- comp defined exactly on indices 1..len
  all i: Int | (1 =< i and i =< len) iff some comp[i]
  -- all components non-negative
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- T4: valid address tumbler
pred T4[t: Tumbler] {
  -- at most three zero-valued field separators
  #{i: Int | 1 =< i and i =< t.len and t.comp[i] = 0} =< 3

  -- every non-separator component is strictly positive
  all i: Int | (1 =< i and i =< t.len and not (t.comp[i] = 0))
    implies t.comp[i] > 0

  -- first field non-empty (first component positive)
  t.comp[1] > 0

  -- last field non-empty (last component positive)
  t.comp[t.len] > 0

  -- no consecutive zeros (no empty interior field)
  all i: Int | (1 =< i and i < t.len and t.comp[i] = 0)
    implies t.comp[plus[i, 1]] > 0
}

-- sig(t) = max({i : 1 <= i <= #t, t_i != 0})
-- Modeled as: s is the significance of t
pred isSig[t: Tumbler, s: Int] {
  1 =< s
  s =< t.len
  not (t.comp[s] = 0)
  all j: Int | (j > s and j =< t.len) implies t.comp[j] = 0
}

-- TA5-SigValid: T4 implies sig(t) = #t
assert SigOnValidAddresses {
  all t: Tumbler | T4[t] implies isSig[t, t.len]
}

-- Non-vacuity: a T4-valid tumbler exists
run NonVacuity {
  some t: Tumbler | T4[t]
} for 5 but exactly 1 Tumbler, 5 Int

check SigOnValidAddresses for 5 but 5 Int
