-- TA2 — WellDefinedSubtraction
-- For tumblers a, w where a >= w, a ⊖ w yields a well-defined (non-negative) result.
--
-- TumblerSubtract: zero-pad to n = max(#a, #w), then:
--   Case 1 (a = w after padding): result = zero tumbler of length n
--   Case 2 (diverge at k):
--     result[i] = 0          for i < k
--     result[k] = a[k]-w[k]  at k
--     result[i] = a[i]       for i > k
-- Precondition (tGeq): at the first divergence k, a[k] >= w[k]
--   (equivalently a[k] > w[k] since they differ at k)

sig Tumbler {
  comps: seq Int
} {
  all i: comps.inds | comps[i] >= 0
}

-- Padded component access: comps[i] if i is a valid index, else 0
fun pget[t: Tumbler, i: Int]: Int {
  (i >= 0 and i < #(t.comps)) => t.comps[i] else 0
}

-- Padded length: max(#a.comps, #w.comps)
fun plen[a, w: Tumbler]: Int {
  let la = #(a.comps), lw = #(w.comps) |
  la >= lw => la else lw
}

-- a >= w: equal after padding, or a leads at the first divergence point
pred tGeq[a, w: Tumbler] {
  let n = plen[a, w] |
  (all i: Int | i >= 0 and i < n implies pget[a, i] = pget[w, i])
  or
  (some k: Int |
    k >= 0 and k < n and
    pget[a, k] > pget[w, k] and
    (all j: Int | j >= 0 and j < k implies pget[a, j] = pget[w, j]))
}

-- r is the result of subtracting w from a, assuming tGeq[a, w]
pred isResult[a, w: Tumbler, r: seq Int] {
  let n = plen[a, w] | {
    #r = n
    -- Case 1: a = w after padding -> zero result
    (
      (all i: Int | i >= 0 and i < n implies pget[a, i] = pget[w, i]) and
      (all i: r.inds | r[i] = 0)
    )
    or
    -- Case 2: first divergence at k, a[k] > w[k]
    (some k: Int | {
      k >= 0
      k < n
      pget[a, k] > pget[w, k]
      all j: Int | j >= 0 and j < k implies pget[a, j] = pget[w, j]
      all i: r.inds | i < k implies r[i] = 0
      r[k] = minus[pget[a, k], pget[w, k]]
      all i: r.inds | i > k implies r[i] = pget[a, i]
    })
  }
}

-- Packages a valid subtraction: tGeq holds and result follows the definition
sig SubtractOp {
  a, w: Tumbler,
  result: seq Int
} {
  tGeq[a, w]
  isResult[a, w, result]
}

-- TA2: all components of the subtraction result are non-negative
assert TA2_WellDefinedSubtraction {
  all op: SubtractOp |
    all i: op.result.inds | op.result[i] >= 0
}

-- Non-vacuity: a non-empty subtraction result can be found
run NonVacuous {
  some op: SubtractOp | some op.result.inds
} for 4 but 4 Int, 3 seq

check TA2_WellDefinedSubtraction for 4 but 4 Int, 3 seq
