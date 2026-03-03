-- ReverseInverse: (a ⊖ w) ⊕ w = a
-- Conditions: w > 0, #a = #w = k (1-based), action point of w = k (last position),
--             all components of a before k are 0, a ≥ w.

sig Tumbler {
  comps: seq Int
}

fact NonNeg {
  all t: Tumbler | all i: t.comps.inds | t.comps[i] >= 0
}

pred positive[t: Tumbler] {
  some i: t.comps.inds | not (t.comps[i] = 0)
}

-- 0-based index of first nonzero component; precondition: t is positive
fun actionPoint[t: Tumbler]: Int {
  min[{i: t.comps.inds | not (t.comps[i] = 0)}]
}

-- Component-wise equality of two tumblers
pred tEq[a, b: Tumbler] {
  #a.comps = #b.comps
  all i: a.comps.inds | a.comps[i] = b.comps[i]
}

-- TumblerAdd: result = a ⊕ w
pred TAdd[a, w, result: Tumbler] {
  positive[w]
  let k = actionPoint[w] | {
    k in a.comps.inds
    #result.comps = #w.comps
    all i: result.comps.inds | {
      i < k implies result.comps[i] = a.comps[i]
      i = k implies result.comps[i] = plus[a.comps[k], w.comps[k]]
      i > k implies result.comps[i] = w.comps[i]
    }
  }
}

-- TumblerSubtract: result = a ⊖ w (equal-length tumblers; zero-padding is a no-op)
pred TSub[a, w, result: Tumbler] {
  #a.comps = #w.comps
  #result.comps = #a.comps
  tEq[a, w] implies {
    all i: result.comps.inds | result.comps[i] = 0
  }
  not tEq[a, w] implies {
    let k = min[{i: a.comps.inds | not (a.comps[i] = w.comps[i])}] | {
      all i: result.comps.inds | {
        i < k implies result.comps[i] = 0
        i = k implies result.comps[i] = minus[a.comps[k], w.comps[k]]
        i > k implies result.comps[i] = a.comps[i]
      }
    }
  }
}

-- Preconditions for ReverseInverse:
--   w > 0
--   #a = #w = k (1-based length), where k = action point of w
--   action point of w is the last position (0-based: #w - 1)
--   all components of a before the last are 0
--   a ≥ w (at the only possible divergence — the last position — a_last ≥ w_last)
pred pre[a, w: Tumbler] {
  positive[w]
  #a.comps = #w.comps
  #a.comps > 0
  actionPoint[w] = minus[#w.comps, 1]
  all i: a.comps.inds | i < minus[#a.comps, 1] implies a.comps[i] = 0
  a.comps[minus[#a.comps, 1]] >= w.comps[minus[#w.comps, 1]]
}

assert ReverseInverse {
  all a, w, diff, result: Tumbler |
    (pre[a, w] and TSub[a, w, diff] and TAdd[diff, w, result])
    implies tEq[result, a]
}

-- Non-vacuity: confirm the preconditions are satisfiable
run {
  some a, w, diff, result: Tumbler |
    pre[a, w] and TSub[a, w, diff] and TAdd[diff, w, result]
} for 5 but 4 seq, 5 Int

check ReverseInverse for 5 but 4 seq, 5 Int
