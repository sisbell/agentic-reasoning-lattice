-- T4 — HierarchicalParsing
-- Every I-space address tumbler has at most three zero-valued
-- components acting as field separators. Non-separator components
-- are strictly positive. The zero count determines hierarchical level.

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fact WellFormed {
  all t: Tumbler {
    t.len >= 1
    all i: Int | (i >= 1 and i =< t.len) implies one t.comp[i]
    all i: Int | (i < 1 or i > t.len) implies no t.comp[i]
    all i: Int | some t.comp[i] implies t.comp[i] >= 0
  }
}

-- Count of zero-valued components
fun zeros[t: Tumbler]: Int {
  #{i: Int | i >= 1 and i =< t.len and t.comp[i] = 0}
}

-- I-space address invariant: at most 3 isolated interior zeros
pred isISpaceAddr[t: Tumbler] {
  -- at most three zero separators
  zeros[t] =< 3
  -- first and last components are positive (zeros are interior)
  t.comp[1] > 0
  t.comp[t.len] > 0
  -- no consecutive zeros (each separator divides non-empty fields)
  all i: Int | (i >= 1 and i < t.len and t.comp[i] = 0)
    implies t.comp[plus[i, 1]] > 0
}

-- Level classification by zero count
pred isNodeAddr[t: Tumbler] { isISpaceAddr[t] and zeros[t] = 0 }
pred isUserAddr[t: Tumbler] { isISpaceAddr[t] and zeros[t] = 1 }
pred isDocAddr[t: Tumbler]  { isISpaceAddr[t] and zeros[t] = 2 }
pred isElemAddr[t: Tumbler] { isISpaceAddr[t] and zeros[t] = 3 }

-- T4a: level classification is exhaustive
assert LevelPartition {
  all t: Tumbler | isISpaceAddr[t] implies
    (isNodeAddr[t] or isUserAddr[t] or isDocAddr[t] or isElemAddr[t])
}

-- T4b: levels are mutually exclusive
assert LevelExclusive {
  no t: Tumbler |
    (isNodeAddr[t] and isUserAddr[t]) or
    (isNodeAddr[t] and isDocAddr[t]) or
    (isNodeAddr[t] and isElemAddr[t]) or
    (isUserAddr[t] and isDocAddr[t]) or
    (isUserAddr[t] and isElemAddr[t]) or
    (isDocAddr[t] and isElemAddr[t])
}

-- T4c: between consecutive zero separators, at least one
-- positive component exists (fields are non-empty)
assert FieldsNonEmpty {
  all t: Tumbler | isISpaceAddr[t] implies
    all i, j: Int |
      (i >= 1 and j >= 1 and i =< t.len and j =< t.len and
       t.comp[i] = 0 and t.comp[j] = 0 and i < j and
       (no k: Int | k > i and k < j and k >= 1 and k =< t.len
                     and t.comp[k] = 0))
      implies
      (some k: Int | k > i and k < j and t.comp[k] > 0)
}

-- T4d: node address (zeros=0) has only positive components
assert NodeAddrAllPositive {
  all t: Tumbler | isNodeAddr[t] implies
    (all i: Int | (i >= 1 and i =< t.len) implies t.comp[i] > 0)
}

-- Non-vacuity: instances at each level
run FindNodeAddr {
  some t: Tumbler | isNodeAddr[t]
} for 3 but 5 Int

run FindElemAddr {
  some t: Tumbler | isElemAddr[t]
} for 3 but 5 Int

check LevelPartition for 4 but 5 Int
check LevelExclusive for 4 but 5 Int
check FieldsNonEmpty for 4 but 5 Int
check NodeAddrAllPositive for 4 but 5 Int
