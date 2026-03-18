-- TA4 — MutualInverse
-- Check: (a ⊕ w) ⊖ w = a under the TA4 preconditions:
--   w > 0, k = actionPoint(w), k = #a, #w = k, a[i]=0 for all 1 ≤ i < k (1-based)
--
-- Encoding uses 0-based indices throughout.
-- k0 denotes the 0-based action point (= spec's k − 1).
-- TA4 precondition in 0-based terms:
--   #a.comps = k0+1, #w.comps = k0+1,
--   w[k0] ≠ 0, w[i]=0 for i < k0,
--   a[i]=0 for i < k0.

sig Tumbler {
  comps: seq Int
} {
  all i: comps.inds | comps[i] >= 0
}

-- t has at least one nonzero component
pred isPositive[t: Tumbler] {
  some i: t.comps.inds | not (t.comps[i] = 0)
}

-- k0 is the 0-based action point of w:
-- the first index that is nonzero, with all prior indices zero
pred isActionPoint0[w: Tumbler, k0: Int] {
  k0 in w.comps.inds
  not (w.comps[k0] = 0)
  all i: w.comps.inds | i < k0 implies w.comps[i] = 0
}

-- TA4 precondition
pred ta4Pre[a: Tumbler, w: Tumbler, k0: Int] {
  isPositive[w]
  isActionPoint0[w, k0]
  -- #a = k and #w = k, where k = k0+1 (1-based length)
  #a.comps = plus[k0, 1]
  #w.comps = plus[k0, 1]
  -- all components of a before the action point are zero
  all i: a.comps.inds | i < k0 implies a.comps[i] = 0
}

-- TumblerAdd: r = a ⊕ w, with k0 the 0-based action point of w
-- Under ta4Pre: #r = #w = k0+1; no tail beyond k0 in w
pred tAdd[a: Tumbler, w: Tumbler, k0: Int, r: Tumbler] {
  #r.comps = #w.comps
  all i: r.comps.inds | i < k0 implies r.comps[i] = a.comps[i]
  r.comps[k0] = plus[a.comps[k0], w.comps[k0]]
  all i: r.comps.inds | i > k0 implies r.comps[i] = w.comps[i]
}

-- Component-wise equality for same-length tumblers
pred tupleEq[t1: Tumbler, t2: Tumbler] {
  #t1.comps = #t2.comps
  all i: t1.comps.inds | t1.comps[i] = t2.comps[i]
}

-- TumblerSubtract: r = b ⊖ w
-- Assumes #b = #w (no zero-padding needed — holds by construction in TA4)
pred tSub[b: Tumbler, w: Tumbler, r: Tumbler] {
  #r.comps = #b.comps
  -- Case: b = w (zero result)
  tupleEq[b, w] implies
    (all i: r.comps.inds | r.comps[i] = 0)
  -- Case: b ≠ w (diverge at first differing index)
  not tupleEq[b, w] implies
    (some kd: Int |
      kd in b.comps.inds and
      not (b.comps[kd] = w.comps[kd]) and
      (all i: b.comps.inds | i < kd implies b.comps[i] = w.comps[i]) and
      (all i: r.comps.inds | i < kd implies r.comps[i] = 0) and
      r.comps[kd] = minus[b.comps[kd], w.comps[kd]] and
      (all i: r.comps.inds | i > kd implies r.comps[i] = b.comps[i]))
}

-- TA4: the round-trip (a ⊕ w) ⊖ w equals a
assert TA4_MutualInverse {
  all a, w, r1, r2: Tumbler, k0: Int |
    (ta4Pre[a, w, k0] and tAdd[a, w, k0, r1] and tSub[r1, w, r2])
    implies tupleEq[r2, a]
}

-- Non-vacuity: confirm the preconditions are jointly satisfiable
run FindTA4Instance {
  some a, w, r1, r2: Tumbler, k0: Int |
    ta4Pre[a, w, k0] and tAdd[a, w, k0, r1] and tSub[r1, w, r2]
} for 5 but 5 Int

check TA4_MutualInverse for 5 but 5 Int
