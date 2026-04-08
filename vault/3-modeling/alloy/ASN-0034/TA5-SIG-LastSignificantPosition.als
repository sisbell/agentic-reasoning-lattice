open util/integer

-- Tumbler: sequence of non-negative integers, length >= 1
sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  -- comp defined exactly on positions 1..len
  all i: Int | (i >= 1 and i =< len) iff some comp[i]
  -- all component values are non-negative
  all i: Int | some comp[i] implies comp[i] >= 0
}

-- TA5-SIG: Last significant position
-- sig(t) = max({i : 1 <= i <= #t and t_i != 0}) when some nonzero component exists
-- sig(t) = #t when all components are zero
fun lastSig[t: Tumbler]: Int {
  let nonzero = {i: Int | i >= 1 and i =< t.len and not (t.comp[i] = 0)} |
    some nonzero => max[nonzero] else t.len
}

-- Range property from contract: 1 <= sig(t) <= #t
assert SigInRange {
  all t: Tumbler |
    lastSig[t] >= 1 and lastSig[t] =< t.len
}

-- Nonzero case: sig is at a nonzero position and all positions after it are zero
assert SigNonzeroCase {
  all t: Tumbler |
    (some i: Int | i >= 1 and i =< t.len and not (t.comp[i] = 0))
    implies (
      not (t.comp[lastSig[t]] = 0)
      and
      (all j: Int | (j > lastSig[t] and j =< t.len) implies t.comp[j] = 0)
    )
}

-- Zero case: when every component is zero, sig(t) = #t
assert SigZeroCase {
  all t: Tumbler |
    (all i: Int | (i >= 1 and i =< t.len) implies t.comp[i] = 0)
    implies lastSig[t] = t.len
}

-- Non-vacuity: find a tumbler with at least one nonzero component
run FindSigNonzero {
  some t: Tumbler |
    some i: Int | i >= 1 and i =< t.len and not (t.comp[i] = 0)
} for 5 but exactly 1 Tumbler, 5 Int

check SigInRange for 5 but 5 Int
check SigNonzeroCase for 5 but 5 Int
check SigZeroCase for 5 but 5 Int
