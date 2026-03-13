-- TA7a — SubspaceClosure
-- Single-component tumbler arithmetic is closed within a subspace.
-- In the ordinal-only formulation, positions are [x] and displacements
-- are [n] with n > 0.  Arithmetic reduces to integer add/subtract
-- and the result stays in the subspace (or is the zero tumbler).

open util/integer

-- Single-component tumbler [x] with x >= 0
sig Tumbler {
  ord: Int
} {
  ord >= 0
}

-- Positive tumbler: at least one nonzero component
pred positive[t: Tumbler] {
  t.ord > 0
}

-- TumblerAdd for single-component: [x] ⊕ [n] = [x + n]
-- Action point k = 1, result length = 1
pred Add[a, w, result: Tumbler] {
  w.ord > 0                            -- positive displacement
  result.ord = plus[a.ord, w.ord]      -- single-component addition
}

-- TumblerSubtract for single-component: [x] ⊖ [n] = [x - n]
-- Precondition: x >= n
pred Sub[a, w, result: Tumbler] {
  w.ord > 0                            -- positive displacement
  a.ord >= w.ord                       -- precondition
  result.ord = minus[a.ord, w.ord]     -- single-component subtraction
}

-- TA7a part 1: addition closure
-- For all [x] in S, n > 0: [x] ⊕ [n] = [x + n] ∈ S
-- (result is positive, hence in the subspace)
assert AddClosure {
  all a, w, result: Tumbler |
    (positive[a] and Add[a, w, result])
      implies positive[result]
}

-- TA7a part 2: subtraction closure
-- For all [x] in S, n > 0, x >= n: [x] ⊖ [n] ∈ S ∪ {[0]}
-- (result is non-negative: either positive or the zero tumbler)
assert SubClosure {
  all a, w, result: Tumbler |
    (positive[a] and Sub[a, w, result])
      implies (positive[result] or result.ord = 0)
}

-- Non-vacuity: find a valid addition
run FindAdd {
  some a, w, result: Tumbler |
    positive[a] and Add[a, w, result] and positive[result]
} for 4 but 5 Int

-- Non-vacuity: find subtraction yielding zero (edge case x = n)
run FindSubToZero {
  some a, w, result: Tumbler |
    positive[a] and Sub[a, w, result] and result.ord = 0
} for 4 but 5 Int

check AddClosure for 5 but 5 Int
check SubClosure for 5 but 5 Int
