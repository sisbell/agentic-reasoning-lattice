-- ASN-0034 Property T0a: UnboundedComponentValues
-- For every tumbler t and position i (1 <= i <= #t), for every bound M >= 0,
-- there exists t' in T agreeing with t at all positions except i, where t'_i > M.
--
-- Alloy integers are bounded by bitwidth, so this inherently unbounded property
-- will produce counterexamples at the scope boundary. This is expected.

open util/ordering[Pos] as po

-- Positions within a tumbler (ordered)
sig Pos {}

-- A tumbler: finite sequence of naturals with length >= 1
sig Tumbler {
  len: one Pos,
  comp: Pos -> one Int
} {
  -- Valid positions hold natural numbers
  all p: Pos | validPos[this, p] implies comp[p] >= 0
  -- Positions beyond length are zero
  all p: Pos | not validPos[this, p] implies comp[p] = 0
}

-- Position p is within the length of tumbler t
pred validPos[t: Tumbler, p: Pos] {
  p in po/prevs[t.len] + t.len
}

-- tPrime witnesses unboundedness: same length, agrees everywhere except pos, exceeds M at pos
pred witness[t: Tumbler, tPrime: Tumbler, pos: Pos, M: Int] {
  -- Same length
  tPrime.len = t.len
  -- Agrees at all valid positions except pos
  all p: Pos | (validPos[t, p] and p != pos) implies tPrime.comp[p] = t.comp[p]
  -- At pos, component exceeds M
  tPrime.comp[pos] > M
}

-- T0a: UnboundedComponentValues
assert UnboundedComponentValues {
  all t: Tumbler, pos: Pos, M: Int |
    (validPos[t, pos] and M >= 0) implies
      (some tPrime: Tumbler | witness[t, tPrime, pos, M])
}

-- Non-vacuity: a witness exists for some tumbler, position, and bound
run NonVacuity {
  some t, tPrime: Tumbler, pos: Pos, M: Int |
    validPos[t, pos] and M >= 0 and witness[t, tPrime, pos, M]
} for 4 but exactly 2 Tumbler, 3 Pos, 5 Int

check UnboundedComponentValues for 4 but 6 Tumbler, 3 Pos, 5 Int
