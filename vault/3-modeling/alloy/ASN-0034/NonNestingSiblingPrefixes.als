-- T10a.2 NonNestingSiblingPrefixes
-- Distinct siblings from the same allocator are prefix-incomparable:
-- ti ⋠ tj ∧ tj ⋠ ti.

open util/integer

sig Tumbler {
  len: Int,
  digitAt: Int -> lone Int
} {
  len >= 1
  -- digits defined exactly at positions 1..len
  all i: Int | (i >= 1 and i =< len) implies one digitAt[i]
  all i: Int | (i < 1 or i > len) implies no digitAt[i]
  -- digit values are non-negative
  all i: Int | some digitAt[i] implies digitAt[i] >= 0
}

-- Value semantics: structurally identical tumblers are the same atom
fact TumblersAreValueTyped {
  all t1, t2: Tumbler |
    (t1.len = t2.len and
     (all i: Int | (i >= 1 and i =< t1.len) implies t1.digitAt[i] = t2.digitAt[i]))
    implies t1 = t2
}

-- Prefix relation: a ≼ b
pred isPrefix[a, b: Tumbler] {
  a.len =< b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.digitAt[i] = b.digitAt[i]
}

-- Allocator whose siblings all share the same length (T10a.1 precondition)
sig Allocator {
  siblings: set Tumbler
} {
  all t1, t2: siblings | t1.len = t2.len
}

-- T10a.2: Distinct siblings from the same allocator are prefix-incomparable
assert NonNestingSiblingPrefixes {
  all a: Allocator, ti, tj: a.siblings |
    ti != tj implies (not isPrefix[ti, tj] and not isPrefix[tj, ti])
}

-- Non-vacuity: an allocator with at least 2 distinct siblings exists
run NonVacuity {
  some a: Allocator | #a.siblings >= 2
} for 4 but exactly 1 Allocator, 5 Int

check NonNestingSiblingPrefixes for 5 but exactly 1 Allocator, 5 Int
