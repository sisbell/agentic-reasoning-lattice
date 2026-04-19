-- TA7a SubspaceClosure: arithmetic on ordinals, with the subspace
-- identifier held as structural context, produces results in T.
-- S = {o in T : #o >= 1 and all components > 0}.

open util/integer

sig Tumbler {
  len: Int,
  c1: Int,
  c2: Int,
  c3: Int
}

fact TumblerWF {
  all t: Tumbler {
    t.len >= 1 and t.len =< 3
    t.c1 >= 0 and t.c2 >= 0 and t.c3 >= 0
    t.c1 =< 7 and t.c2 =< 7 and t.c3 =< 7
    t.len =< 1 implies t.c2 = 0
    t.len =< 2 implies t.c3 = 0
  }
}

-- S membership: all components positive
pred inS[t: Tumbler] {
  t.c1 > 0
  t.len >= 2 implies t.c2 > 0
  t.len >= 3 implies t.c3 > 0
}

-- Positive tumbler: at least one nonzero component
pred isPos[t: Tumbler] {
  t.c1 > 0 or t.c2 > 0 or t.c3 > 0
}

-- Action point: first 1-indexed position with nonzero component.
-- Only meaningful when isPos holds.
fun actPt[w: Tumbler]: Int {
  w.c1 != 0 => 1 else (w.c2 != 0 => 2 else 3)
}

-- Zero-padded divergence: first position where components differ.
-- Returns 0 when all zero-padded components agree.
fun zpd[a, b: Tumbler]: Int {
  a.c1 != b.c1 => 1 else
  (a.c2 != b.c2 => 2 else
  (a.c3 != b.c3 => 3 else 0))
}

-- Tumbler ordering via zero-padded comparison: a >= b.
pred geq[a, b: Tumbler] {
  let d = zpd[a, b] |
  d = 0 or
  (d = 1 and a.c1 > b.c1) or
  (d = 2 and a.c2 > b.c2) or
  (d = 3 and a.c3 > b.c3)
}

------------------------------------------------------------
-- TumblerAdd (oplus) result components
-- r_i = o_i for i < k; r_k = o_k + w_k; r_i = w_i for i > k
-- Result length = #w
------------------------------------------------------------

fun addR1[o, w: Tumbler]: Int {
  let k = actPt[w] |
  k = 1 => plus[o.c1, w.c1] else o.c1
}

fun addR2[o, w: Tumbler]: Int {
  let k = actPt[w] |
  k = 2 => plus[o.c2, w.c2] else (k = 1 => w.c2 else o.c2)
}

fun addR3[o, w: Tumbler]: Int {
  let k = actPt[w] |
  k = 3 => plus[o.c3, w.c3] else w.c3
}

------------------------------------------------------------
-- TumblerSub (ominus) result components
-- At zpd d: r_i = 0 for i < d; r_d = o_d - w_d; r_i = o_i for i > d
-- When d = 0 (no divergence): all zeros
-- Result length = max(#o, #w)
------------------------------------------------------------

fun subR1[o, w: Tumbler]: Int {
  let d = zpd[o, w] |
  d = 1 => minus[o.c1, w.c1] else 0
}

fun subR2[o, w: Tumbler]: Int {
  let d = zpd[o, w] |
  d = 2 => minus[o.c2, w.c2] else (d = 1 => o.c2 else 0)
}

fun subR3[o, w: Tumbler]: Int {
  let d = zpd[o, w] |
  d = 3 => minus[o.c3, w.c3] else ((d = 1 or d = 2) => o.c3 else 0)
}

------------------------------------------------------------
-- Helper predicates for S-membership results
------------------------------------------------------------

-- Tail of w (components after action point) all positive
pred tailPos[w: Tumbler] {
  let k = actPt[w] | {
    k = 1 implies {
      w.len >= 2 implies w.c2 > 0
      w.len >= 3 implies w.c3 > 0
    }
    k = 2 implies {
      w.len >= 3 implies w.c3 > 0
    }
  }
}

-- Addition result has all components positive up to result length
pred addInS[o, w: Tumbler] {
  addR1[o, w] > 0
  w.len >= 2 implies addR2[o, w] > 0
  w.len >= 3 implies addR3[o, w] > 0
}

------------------------------------------------------------
-- Assertions
------------------------------------------------------------

-- Conjunct 1: oplus-closure in T (non-negative components)
assert AddClosureT {
  all o, w: Tumbler |
    (inS[o] and isPos[w] and actPt[w] =< o.len) implies
    (addR1[o, w] >= 0 and addR2[o, w] >= 0 and addR3[o, w] >= 0)
}

-- Strengthened: oplus result in S when tail of w is positive
assert AddClosureS {
  all o, w: Tumbler |
    (inS[o] and isPos[w] and actPt[w] =< o.len and tailPos[w]) implies
    addInS[o, w]
}

-- Conjunct 2: ominus-closure in T (non-negative components)
assert SubClosureT {
  all o, w: Tumbler |
    (inS[o] and isPos[w] and geq[o, w]) implies
    (subR1[o, w] >= 0 and subR2[o, w] >= 0 and subR3[o, w] >= 0)
}

-- actPt >= 2, #w =< #o: subtraction is a no-op (result = o)
assert SubNoOpK2 {
  all o, w: Tumbler |
    (inS[o] and isPos[w] and geq[o, w] and
     actPt[w] >= 2 and w.len =< o.len) implies
    (subR1[o, w] = o.c1 and subR2[o, w] = o.c2 and subR3[o, w] = o.c3)
}

-- actPt = 1, zpd = 1, #w =< #o: result in S
assert SubSK1D1 {
  all o, w: Tumbler |
    (inS[o] and isPos[w] and geq[o, w] and
     actPt[w] = 1 and zpd[o, w] = 1 and w.len =< o.len) implies
    (subR1[o, w] > 0 and
     (o.len >= 2 implies subR2[o, w] > 0) and
     (o.len >= 3 implies subR3[o, w] > 0))
}

-- actPt = 1, zpd > 1: first component is 0, hence not in S
assert SubNotSK1DGt1 {
  all o, w: Tumbler |
    (inS[o] and isPos[w] and geq[o, w] and
     actPt[w] = 1 and zpd[o, w] > 1) implies
    subR1[o, w] = 0
}

-- Single-component: result in S when o1 > w1, zero when o1 = w1
assert SubSingleSZ {
  all o, w: Tumbler |
    (o.len = 1 and w.len = 1 and inS[o] and isPos[w] and geq[o, w]) implies
    ((o.c1 > w.c1 implies subR1[o, w] > 0) and
     (o.c1 = w.c1 implies subR1[o, w] = 0))
}

-- #w > #o: trailing result components (positions #o+1 through #w) are zero,
-- hence result lies in T \ S
assert SubTrailingZeros {
  all o, w: Tumbler |
    (inS[o] and isPos[w] and geq[o, w] and w.len > o.len) implies
    (o.len =< 1 implies subR2[o, w] = 0) and
    (o.len =< 2 implies subR3[o, w] = 0)
}

------------------------------------------------------------
-- Non-vacuity runs
------------------------------------------------------------

run FindAdd {
  some o, w: Tumbler |
    inS[o] and isPos[w] and actPt[w] =< o.len
} for 5 but 5 Int

run FindSub {
  some o, w: Tumbler |
    inS[o] and isPos[w] and geq[o, w]
} for 5 but 5 Int

-- Verify spec counterexample: [5,3] ominus [5,1] = [0,2]
run CounterexK1DGt1 {
  some o, w: Tumbler |
    o.len = 2 and o.c1 = 5 and o.c2 = 3 and
    w.len = 2 and w.c1 = 5 and w.c2 = 1 and
    subR1[o, w] = 0 and subR2[o, w] = 2
} for 5 but 5 Int

-- Non-vacuity for #w > #o: o=[3] (len=1), w=[0,2] (len=2, k=2)
run FindSubLongW {
  some o, w: Tumbler |
    inS[o] and isPos[w] and geq[o, w] and w.len > o.len
} for 5 but 5 Int

------------------------------------------------------------
-- Checks
------------------------------------------------------------

check AddClosureT for 5 but 5 Int
check AddClosureS for 5 but 5 Int
check SubClosureT for 5 but 5 Int
check SubNoOpK2 for 5 but 5 Int
check SubSK1D1 for 5 but 5 Int
check SubNotSK1DGt1 for 5 but 5 Int
check SubSingleSZ for 5 but 5 Int
check SubTrailingZeros for 5 but 5 Int
