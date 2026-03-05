-- TA7a: SubspaceClosure
-- Single-component tumbler shift arithmetic is closed within subspaces.
-- A subspace S₁ contains all positive ordinals for a structural identifier N.
-- In ordinal-only formulation, N is held as context; arithmetic touches only x.
--   Addition:    (A [x] in S₁, n > 0 : [x] + [n] = [x+n] in S₁)
--   Subtraction: (A [x] in S₁, n > 0, x >= n : [x] - [n] = [x-n] in S₁ ∪ {[0]})

--------------------------------------------------------------
-- Tumbler representation
--------------------------------------------------------------

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
}

fun MAXLEN: Int { 4 }

fact TumblerWF {
  all t: Tumbler {
    t.len >= 1
    t.len =< MAXLEN
    all i: Int | (i >= 1 and i =< t.len) implies one t.comp[i]
    all i: Int | (i < 1 or i > t.len) implies no t.comp[i]
    all i: Int | some t.comp[i] implies t.comp[i] >= 0
  }
}

pred singleComponent[t: Tumbler] { t.len = 1 }

pred positive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] != 0
}

pred isActionPt[w: Tumbler, k: Int] {
  k >= 1 and k =< w.len
  w.comp[k] != 0
  all j: Int | (j >= 1 and j < k) implies w.comp[j] = 0
}

--------------------------------------------------------------
-- TumblerAdd (general definition from ASN)
--------------------------------------------------------------

pred tumblerAdd[a, w, r: Tumbler, k: Int] {
  isActionPt[w, k]
  k =< a.len
  r.len = w.len
  all i: Int | (i >= 1 and i =< r.len) implies
    ((i < k implies r.comp[i] = a.comp[i]) and
     (i = k implies r.comp[i] = plus[a.comp[k], w.comp[k]]) and
     (i > k implies r.comp[i] = w.comp[i]))
}

--------------------------------------------------------------
-- TumblerSubtract (single-component specialization)
-- For len-1 tumblers: divergence is at position 1 (or a = w),
-- so result comp[1] = a.comp[1] - w.comp[1].
--------------------------------------------------------------

pred tumblerSub[a, w, r: Tumbler] {
  singleComponent[a]
  singleComponent[w]
  singleComponent[r]
  w.comp[1] > 0                       -- positive displacement
  a.comp[1] >= w.comp[1]             -- precondition: x >= n
  r.comp[1] = minus[a.comp[1], w.comp[1]]
}

--------------------------------------------------------------
-- Subspace membership
--------------------------------------------------------------

-- S₁ contains single-component tumblers with positive ordinal
pred inSubspace[t: Tumbler] {
  singleComponent[t]
  t.comp[1] > 0
}

-- S₁ ∪ {[0]}: subspace plus the zero single-component tumbler
pred inSubspaceOrZero[t: Tumbler] {
  singleComponent[t]
  t.comp[1] >= 0
}

--------------------------------------------------------------
-- Assertions
--------------------------------------------------------------

-- Addition closure: [x+n] has positive ordinal, stays in S₁
assert AddClosedInSubspace {
  all a, w, r: Tumbler, k: Int |
    (inSubspace[a] and singleComponent[w] and positive[w] and
     tumblerAdd[a, w, r, k] and
     plus[a.comp[1], w.comp[1]] >= 0)       -- Int overflow guard
    implies
    inSubspace[r]
}

-- Addition value: the general TumblerAdd reduces to integer sum
assert AddIsIntegerSum {
  all a, w, r: Tumbler, k: Int |
    (singleComponent[a] and singleComponent[w] and positive[w] and
     tumblerAdd[a, w, r, k] and
     plus[a.comp[1], w.comp[1]] >= 0)
    implies
    r.comp[1] = plus[a.comp[1], w.comp[1]]
}

-- Subtraction closure: [x-n] is in S₁ ∪ {[0]}
assert SubClosedInSubspaceOrZero {
  all a, w, r: Tumbler |
    (inSubspace[a] and tumblerSub[a, w, r])
    implies
    inSubspaceOrZero[r]
}

--------------------------------------------------------------
-- Non-vacuity
--------------------------------------------------------------

run nonVacuousAdd {
  some a, w, r: Tumbler, k: Int |
    inSubspace[a] and singleComponent[w] and positive[w] and
    tumblerAdd[a, w, r, k] and
    plus[a.comp[1], w.comp[1]] >= 0
} for 5 but exactly 3 Tumbler, 5 Int

run nonVacuousSub {
  some a, w, r: Tumbler |
    inSubspace[a] and tumblerSub[a, w, r]
} for 5 but exactly 3 Tumbler, 5 Int

--------------------------------------------------------------
-- Checks
--------------------------------------------------------------

check AddClosedInSubspace for 5 but 5 Int
check AddIsIntegerSum for 5 but 5 Int
check SubClosedInSubspaceOrZero for 5 but 5 Int
