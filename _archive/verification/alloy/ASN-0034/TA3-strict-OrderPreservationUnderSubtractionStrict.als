-- TA3-strict: OrderPreservationUnderSubtractionStrict
-- (A a, b, w : a < b AND a >= w AND b >= w AND #a = #b : a ominus w < b ominus w)

open util/integer

sig Tumbler {
  comp: Int -> lone Int,
  len: one Int
}

one sig A, B, W, RA, RB extends Tumbler {}

fact WellFormed {
  all t: Tumbler {
    t.len >= 1 and t.len =< 3
    all i: Int | (i >= 1 and i =< t.len) iff one t.comp[i]
    all i: Int | (i >= 1 and i =< t.len) implies t.comp[i] >= 0
  }
}

-- Zero-padded component: value at position i, or 0 if beyond length
fun zpad[t: Tumbler, i: Int]: Int {
  (i >= 1 and i =< t.len) => t.comp[i] else 0
}

-- Tumbler strict less-than (T1 ordering)
-- Case (i): first disagreement within shared length, a_k < b_k
-- Case (ii): a is proper prefix of b
pred tLt[a, b: Tumbler] {
  let minLen = (a.len =< b.len => a.len else b.len) | {
    (some k: Int {
      k >= 1 and k =< minLen
      all i: Int | (i >= 1 and i < k) implies a.comp[i] = b.comp[i]
      a.comp[k] < b.comp[k]
    })
    or
    ((all i: Int | (i >= 1 and i =< minLen) implies a.comp[i] = b.comp[i]) and
      a.len < b.len)
  }
}

-- Tumbler value equality
pred tEq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.comp[i] = b.comp[i]
}

-- Tumbler greater-than-or-equal
pred tGe[a, b: Tumbler] {
  tLt[b, a] or tEq[a, b]
}

-- Zero-padded divergence: first position where zero-padded values differ
fun zpd[a, w: Tumbler]: lone Int {
  let maxLen = (a.len >= w.len => a.len else w.len) |
  { d: Int |
    d >= 1 and d =< maxLen and
    not (zpad[a, d] = zpad[w, d]) and
    (all i: Int | (i >= 1 and i < d) implies zpad[a, i] = zpad[w, i])
  }
}

-- Tumbler subtraction: result = a ominus w
pred tSub[a, w, result: Tumbler] {
  let maxLen = (a.len >= w.len => a.len else w.len) |
  let d = zpd[a, w] | {
    result.len = maxLen
    no d => {
      -- No divergence: zero tumbler
      all i: Int | (i >= 1 and i =< maxLen) implies result.comp[i] = 0
    } else {
      -- Divergence at position d
      all i: Int | (i >= 1 and i =< maxLen) implies {
        (i < d) implies result.comp[i] = 0
        (i = d) implies result.comp[i] = minus[zpad[a, d], zpad[w, d]]
        (i > d) implies result.comp[i] = zpad[a, i]
      }
    }
  }
}

-- Constrain RA = A ominus W, RB = B ominus W
fact SubResults {
  tSub[A, W, RA]
  tSub[B, W, RB]
}

-- TA3-strict: subtraction preserves strict order for equal-length tumblers
assert TA3Strict {
  (tLt[A, B] and tGe[A, W] and tGe[B, W] and A.len = B.len)
    implies tLt[RA, RB]
}

-- Non-vacuity: the preconditions are satisfiable
run NonVacuity {
  tLt[A, B] and tGe[A, W] and tGe[B, W] and A.len = B.len
} for 5 but exactly 5 Tumbler, 4 Int

check TA3Strict for 5 but exactly 5 Tumbler, 4 Int
