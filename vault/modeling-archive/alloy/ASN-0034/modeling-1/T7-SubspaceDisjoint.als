-- T7 — SubspaceDisjoint
-- Property: (A a, b in T : a.E1 != b.E1 => a != b)
-- The subspace identifier (first component of the element field)
-- separates the address space into disjoint regions.

open util/integer

-- Component values
sig Val {}

-- Tumbler: sequence of components with field structure
sig Tumbler {
  -- Components at integer positions (1-indexed)
  comp: Int -> lone Val,
  -- Length of the tumbler
  len: Int,
  -- Position of E1 (first element-field component), determined by
  -- the zero-separator pattern per FieldParsing definition
  e1Pos: Int
} {
  len >= 1
  -- comp defined exactly on positions 1..len
  all i: Int | some comp[i] iff (1 =< i and i =< len)
  -- e1Pos is a valid position
  1 =< e1Pos
  e1Pos =< len
}

-- E1: first component of the element field
fun e1[t: Tumbler]: Val {
  t.comp[t.e1Pos]
}

-- Extensional tumbler equality: same length, same components everywhere
pred tumblerEq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | a.comp[i] = b.comp[i]
}

-- Field parsing is deterministic: identical component sequences yield
-- identical field structure, hence identical e1Pos.
-- (FieldParsing: e1Pos is uniquely determined by counting zero separators.)
fact fieldParsingDeterministic {
  all a, b: Tumbler |
    tumblerEq[a, b] implies a.e1Pos = b.e1Pos
}

-- T7: different subspace identifiers imply different tumblers
assert SubspaceDisjoint {
  all a, b: Tumbler |
    e1[a] != e1[b] implies not tumblerEq[a, b]
}

check SubspaceDisjoint for 4 but exactly 2 Tumbler, 5 Int

-- Non-vacuity: two tumblers with different E1 exist
run NonVacuity {
  some disj a, b: Tumbler |
    e1[a] != e1[b]
} for 4 but exactly 2 Tumbler, 5 Int
