-- T4: HierarchicalParsing
--
-- An I-space address tumbler contains at most three zero-valued field-separator
-- components; every non-separator component is strictly positive.
-- The count of zeros (0..3) uniquely identifies the hierarchical level:
--   0 zeros -> node address
--   1 zero  -> user address
--   2 zeros -> document address
--   3 zeros -> element address

sig Comp {
  val: Int
}

sig Tumbler {
  comps: seq Comp
}

fun countZeros[t: Tumbler]: Int {
  #{ i: t.comps.inds | (t.comps[i]).val = 0 }
}

pred hierarchicalParsing[t: Tumbler] {
  all i: t.comps.inds | (t.comps[i]).val >= 0
  countZeros[t] =< 3
}

-- A1: Zero count is bounded to at most 3
assert ZerosBounded {
  all t: Tumbler |
    hierarchicalParsing[t] implies countZeros[t] =< 3
}

-- A2: Non-separator (nonzero) components are strictly positive
assert NonZerosPositive {
  all t: Tumbler |
    hierarchicalParsing[t] implies
    all i: t.comps.inds |
      not ((t.comps[i]).val = 0) implies (t.comps[i]).val > 0
}

-- A3: No well-formed tumbler can have four or more separator zeros
assert AtMostThreeSeparators {
  no t: Tumbler |
    hierarchicalParsing[t] and countZeros[t] >= 4
}

-- Non-vacuity: an element-level address (3 separators) is achievable
run FindElementAddress {
  some t: Tumbler |
    hierarchicalParsing[t] and countZeros[t] = 3
} for 8 but exactly 1 Tumbler, 5 Int, 8 seq

check ZerosBounded          for 5 but 5 Int, 8 seq
check NonZerosPositive      for 5 but 5 Int, 8 seq
check AtMostThreeSeparators for 5 but 5 Int, 8 seq
