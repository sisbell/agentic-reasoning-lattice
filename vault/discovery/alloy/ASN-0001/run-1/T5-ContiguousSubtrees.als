-- T5 — ContiguousSubtrees
-- For any tumbler prefix p, the set {t | p ≼ t} is order-convex under ≤:
--   p ≼ a ∧ p ≼ c ∧ a ≤ b ≤ c  ⟹  p ≼ b
--
-- Ordering: lexicographic with missing components treated as 0 (pad semantics),
-- matching the Divergence definition in the ASN.

sig Tumbler {
  comps: seq Int
}

-- All components non-negative (valid tumbler)
pred wf[t: Tumbler] {
  all i: t.comps.inds | t.comps[i] >= 0
}

-- p is a prefix of t: p is no longer than t, and every p-position matches
pred isPrefix[p, t: Tumbler] {
  #p.comps =< #t.comps
  all i: p.comps.inds | p.comps[i] = t.comps[i]
}

-- Component at index i; out-of-bounds yields 0 (zero-padding semantics)
fun paddedComp[t: Tumbler, i: Int]: Int {
  { v: Int |
    (i in t.comps.inds     and v = t.comps[i])
    or
    (i not in t.comps.inds and v = 0)
  }
}

-- Lexicographic ordering with zero-padding for missing components.
-- a ≤ b iff all padded positions are equal, or there exists a first
-- position k where a[k] < b[k] and all prior positions match.
pred lexLeq[a, b: Tumbler] {
  (all i: Int | i >= 0 implies paddedComp[a, i] = paddedComp[b, i])
  or
  (some k: Int | {
    k >= 0
    all j: Int | (j >= 0 and j < k) implies paddedComp[a, j] = paddedComp[b, j]
    paddedComp[a, k] < paddedComp[b, k]
  })
}

-- Assertion: prefix sets are order-convex intervals
assert ContiguousSubtrees {
  all p, a, b, c: Tumbler |
    (wf[p] and wf[a] and wf[b] and wf[c] and
     isPrefix[p, a] and isPrefix[p, c] and
     lexLeq[a, b] and lexLeq[b, c])
    implies isPrefix[p, b]
}

-- Non-vacuity: find an instance where p is a proper non-empty prefix of a,
-- and b lies strictly between a and c
run NonVacuous {
  some p, a, b, c: Tumbler |
    wf[p] and wf[a] and wf[b] and wf[c] and
    isPrefix[p, a] and isPrefix[p, c] and
    lexLeq[a, b] and lexLeq[b, c] and
    #p.comps > 0 and #a.comps > #p.comps
} for 5 but 3 seq, 5 Int

check ContiguousSubtrees for 5 but 3 seq, 5 Int
