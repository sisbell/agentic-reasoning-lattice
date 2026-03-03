-- TA5 — HierarchicalIncrement
-- inc(t, k) produces t' satisfying:
--   (a) t' > t under T1 (lexicographic order)
--   (b) t' agrees with t before the increment point
--   (c) k=0 (sibling): #t' = #t; only sig(t) changes, incremented by 1
--   (d) k>0 (child):  #t' = #t+k; positions #t+1..#t+k-1 are 0; position #t+k is 1
-- TA5 preserves T4 (zeros ≤ 3) when zeros(t) + k − 1 ≤ 3.

sig Tumbler {
  len: one Int,
  comp: Int -> lone Int
} {
  len >= 0
  len =< 5
  -- comp defined exactly on positions 1..len
  all i: Int | some comp[i] iff (i >= 1 and i =< len)
  -- components are non-negative and bounded (keeps scope tractable)
  all i: Int | (i >= 1 and i =< len) implies (comp[i] >= 0 and comp[i] =< 4)
}

-- sig(t): last significant (nonzero) position; equals len when t is all-zero
pred isSigPos[t: Tumbler, s: Int] {
  t.len > 0
  s >= 1
  s =< t.len
  (
    -- some nonzero component exists: s is the rightmost one
    (some i: Int | i >= 1 and i =< t.len and not (t.comp[i] = 0)) and
    not (t.comp[s] = 0) and
    (all j: Int | (j > s and j >= 1 and j =< t.len) implies t.comp[j] = 0)
  ) or (
    -- all components are zero: s = len
    (all i: Int | i >= 1 and i =< t.len implies t.comp[i] = 0) and
    s = t.len
  )
}

-- zeros(t): count of zero components in 1..len
fun zerosCount[t: Tumbler]: Int {
  #{i: Int | i >= 1 and i =< t.len and t.comp[i] = 0}
}

-- T4: at most 3 zero (separator) components
pred T4[t: Tumbler] {
  zerosCount[t] =< 3
}

-- Components of a and b at position i agree, treating out-of-range as 0
pred compAgree[a, b: Tumbler, i: Int] {
  (i >= 1 and i =< a.len and i =< b.len and a.comp[i] = b.comp[i]) or
  (i > a.len and i > b.len) or
  (i > a.len and i >= 1 and i =< b.len and b.comp[i] = 0) or
  (i >= 1 and i =< a.len and i > b.len and a.comp[i] = 0)
}

-- a's component at i strictly less than b's, treating out-of-range as 0
-- (a out-of-range with b > 0 is the only cross-range case, since all values >= 0)
pred compLt[a, b: Tumbler, i: Int] {
  (i >= 1 and i =< a.len and i =< b.len and a.comp[i] < b.comp[i]) or
  (i > a.len and i >= 1 and i =< b.len and b.comp[i] > 0)
}

-- T1: strict lexicographic order on tumblers (missing components treated as 0)
pred ltT1[a, b: Tumbler] {
  some d: Int | {
    d >= 1
    d =< 5
    all i: Int | (i >= 1 and i < d) implies compAgree[a, b, i]
    compLt[a, b, d]
  }
}

-- inc(t, k) = t2: hierarchical increment
pred incOp[t: Tumbler, k: Int, t2: Tumbler] {
  t.len > 0
  k >= 0
  some s: Int | {
    isSigPos[t, s]
    k = 0 implies {
      -- sibling: same length, increment at sig(t)
      t2.len = t.len
      t2.comp[s] = plus[t.comp[s], 1]
      all i: Int | (i >= 1 and i =< t.len and not (i = s)) implies t2.comp[i] = t.comp[i]
    }
    k > 0 implies {
      -- child: extend by k, copy t, fill k-1 zeros, set final to 1
      t2.len = plus[t.len, k]
      all i: Int | (i >= 1 and i =< t.len) implies t2.comp[i] = t.comp[i]
      all i: Int | (i > t.len and i < t2.len) implies t2.comp[i] = 0
      t2.comp[t2.len] = 1
    }
  }
}

-- (a) inc produces a strictly greater tumbler under T1
assert TA5_ProducesGreater {
  all t, t2: Tumbler, k: Int |
    (t.len > 0 and k >= 0 and incOp[t, k, t2]) implies ltT1[t, t2]
}

-- (b) + (c) sibling: only sig(t) changes, incremented by 1
assert TA5_SiblingStructure {
  all t, t2: Tumbler |
    (t.len > 0 and incOp[t, 0, t2]) implies {
      t2.len = t.len and
      some s: Int | {
        isSigPos[t, s]
        t2.comp[s] = plus[t.comp[s], 1]
        all i: Int | (i >= 1 and i =< t.len and not (i = s)) implies t2.comp[i] = t.comp[i]
      }
    }
}

-- (b) + (d) child: copies t, appends k-1 zeros then 1
assert TA5_ChildStructure {
  all t, t2: Tumbler, k: Int |
    (t.len > 0 and k > 0 and incOp[t, k, t2]) implies {
      t2.len = plus[t.len, k] and
      (all i: Int | (i >= 1 and i =< t.len) implies t2.comp[i] = t.comp[i]) and
      (all i: Int | (i > t.len and i < t2.len) implies t2.comp[i] = 0) and
      t2.comp[t2.len] = 1
    }
}

-- T4 preservation: zeros(t) + k - 1 ≤ 3 is the sufficient condition
assert TA5_PreservesT4 {
  all t, t2: Tumbler, k: Int |
    (t.len > 0 and k >= 0 and
     T4[t] and
     plus[zerosCount[t], minus[k, 1]] =< 3 and
     incOp[t, k, t2]) implies T4[t2]
}

-- Non-vacuity: confirm inc is satisfiable for both sibling and child cases
run FindInc {
  some t, t2: Tumbler, k: Int |
    t.len > 0 and k >= 0 and k =< 2 and incOp[t, k, t2]
} for 5 but exactly 2 Tumbler, 4 Int

check TA5_ProducesGreater  for 5 but exactly 2 Tumbler, 4 Int
check TA5_SiblingStructure for 5 but exactly 2 Tumbler, 4 Int
check TA5_ChildStructure   for 5 but exactly 2 Tumbler, 4 Int
check TA5_PreservesT4      for 5 but exactly 2 Tumbler, 4 Int
