-- TA5a (IncrementPreservesT4)
-- inc(t, k) on a valid address t preserves T4 iff
--   k = 0, or k = 1 with zeros(t) <= 3, or k = 2 with zeros(t) <= 2.
-- For k >= 3, T4 is violated (adjacent zeros create an empty field).

open util/integer

-- Tumbler: sequence of non-negative integers indexed 1..len
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  all i: Int | (1 =< i and i =< len) iff some comp[i]
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- Count of zero-valued components (field separators)
fun zeros[t: Tumbler]: Int {
  #{i: Int | 1 =< i and i =< t.len and t.comp[i] = 0}
}

-- T4: valid address tumbler
pred T4[t: Tumbler] {
  -- (i) at most three zero-valued field separators
  zeros[t] =< 3

  -- (ii) every non-separator component is strictly positive
  all i: Int | (1 =< i and i =< t.len and not (t.comp[i] = 0))
    implies t.comp[i] > 0

  -- first component positive
  t.comp[1] > 0

  -- last component positive
  t.comp[t.len] > 0

  -- (iii) no consecutive zeros (no empty interior field)
  all i: Int | (1 =< i and i < t.len and t.comp[i] = 0)
    implies t.comp[plus[i, 1]] > 0
}

-- inc(t, k): increment tumbler t at depth k, producing result
pred inc[t: Tumbler, k: Int, result: Tumbler] {
  k >= 0

  -- Case k = 0: sibling increment — same length, increment last component
  k = 0 implies {
    result.len = t.len
    result.comp[t.len] = plus[t.comp[t.len], 1]
    all i: Int | (1 =< i and i < t.len) implies
      result.comp[i] = t.comp[i]
  }

  -- Case k > 0: child at depth k — extend by k positions
  k > 0 implies {
    result.len = plus[t.len, k]
    -- Copy original components
    all i: Int | (1 =< i and i =< t.len) implies
      result.comp[i] = t.comp[i]
    -- k-1 zero separators at positions len+1 through len+k-1
    all j: Int | (j >= plus[t.len, 1] and j =< minus[plus[t.len, k], 1]) implies
      result.comp[j] = 0
    -- Final component at position len+k is 1
    result.comp[plus[t.len, k]] = 1
  }
}

-- Condition under which T4 is preserved
pred preserveCondition[t: Tumbler, k: Int] {
  k = 0
  or (k = 1 and zeros[t] =< 3)
  or (k = 2 and zeros[t] =< 2)
}

-- Forward: when condition holds, T4 is preserved
assert TA5a_Forward {
  all t, result: Tumbler, k: Int |
    (T4[t] and inc[t, k, result] and preserveCondition[t, k])
      implies T4[result]
}

-- Backward: when condition fails, T4 is violated
assert TA5a_Backward {
  all t, result: Tumbler, k: Int |
    (T4[t] and inc[t, k, result] and not preserveCondition[t, k])
      implies not T4[result]
}

-- Non-vacuity: valid inc with k > 0 exists
run NonVacuity {
  some t, result: Tumbler, k: Int |
    T4[t] and inc[t, k, result] and k > 0
} for 5 but exactly 2 Tumbler, 5 Int

check TA5a_Forward for 5 but exactly 2 Tumbler, 5 Int
check TA5a_Backward for 5 but exactly 2 Tumbler, 5 Int
