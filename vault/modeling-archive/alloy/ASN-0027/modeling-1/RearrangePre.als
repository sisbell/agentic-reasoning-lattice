-- A3.pre — RearrangePre
-- Precondition: d ∈ Σ.D ∧ m ∈ {3,4} ∧ 1 ≤ c1 < c2 < ... < cm ≤ nd + 1

sig Addr {}

sig Doc {
  slots: seq Addr
}

sig State {
  docs: set Doc
}

-- document length
fun nd[d: Doc]: Int {
  #(d.slots)
}

-- Precondition for m = 3
pred RearrangePre3[s: State, d: Doc, c1, c2, c3: Int] {
  d in s.docs
  1 =< c1
  c1 < c2
  c2 < c3
  c3 =< plus[nd[d], 1]
}

-- Precondition for m = 4
pred RearrangePre4[s: State, d: Doc, c1, c2, c3, c4: Int] {
  d in s.docs
  1 =< c1
  c1 < c2
  c2 < c3
  c3 < c4
  c4 =< plus[nd[d], 1]
}

-- Pivot bijection intervals [c1,c2) and [c2,c3) are non-empty
assert PivotIntervalsNonEmpty {
  all s: State, d: Doc, c1, c2, c3: Int |
    RearrangePre3[s, d, c1, c2, c3] implies
      (minus[c2, c1] >= 1 and minus[c3, c2] >= 1)
}

-- Swap bijection intervals [c1,c2), [c2,c3), [c3,c4) are non-empty
assert SwapIntervalsNonEmpty {
  all s: State, d: Doc, c1, c2, c3, c4: Int |
    RearrangePre4[s, d, c1, c2, c3, c4] implies
      (minus[c2, c1] >= 1 and minus[c3, c2] >= 1 and minus[c4, c3] >= 1)
}

-- m=3 requires document length >= 2
assert Pre3MinLength {
  all s: State, d: Doc, c1, c2, c3: Int |
    RearrangePre3[s, d, c1, c2, c3] implies nd[d] >= 2
}

-- m=4 requires document length >= 3
assert Pre4MinLength {
  all s: State, d: Doc, c1, c2, c3, c4: Int |
    RearrangePre4[s, d, c1, c2, c3, c4] implies nd[d] >= 3
}

-- All cuts lie within [1, nd+1]
assert Pre3AllCutsInRange {
  all s: State, d: Doc, c1, c2, c3: Int |
    RearrangePre3[s, d, c1, c2, c3] implies
      (c1 >= 1 and c2 >= 1 and c3 >= 1 and
       c1 =< plus[nd[d], 1] and c2 =< plus[nd[d], 1] and c3 =< plus[nd[d], 1])
}

-- Non-vacuity: find a valid m=3 configuration
run FindPre3 {
  some s: State, d: Doc, c1, c2, c3: Int |
    RearrangePre3[s, d, c1, c2, c3]
} for 4 but exactly 1 State, exactly 1 Doc, 4 seq, 5 Int

-- Non-vacuity: find a valid m=4 configuration
run FindPre4 {
  some s: State, d: Doc, c1, c2, c3, c4: Int |
    RearrangePre4[s, d, c1, c2, c3, c4]
} for 4 but exactly 1 State, exactly 1 Doc, 4 seq, 5 Int

check PivotIntervalsNonEmpty for 5 but exactly 1 State, 4 seq, 5 Int
check SwapIntervalsNonEmpty for 5 but exactly 1 State, 4 seq, 5 Int
check Pre3MinLength for 5 but exactly 1 State, 4 seq, 5 Int
check Pre4MinLength for 5 but exactly 1 State, 4 seq, 5 Int
check Pre3AllCutsInRange for 5 but exactly 1 State, 4 seq, 5 Int
