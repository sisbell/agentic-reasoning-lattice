-- T2 — IntrinsicComparison
-- The lexicographic order (T1) is computable from the two tumblers alone;
-- the comparison examines at most min(#a.comps, #b.comps) component pairs.
--
-- Three assertions:
--   BoundedWitness          — the divergence witness k <= min(len(a), len(b))
--   PrefixAgreementDetermines — if all common positions agree, length decides order
--   Deterministic           — result depends only on component sequences (intrinsic)

sig Tumbler {
  comps: seq Int
}

-- Tumbler components are natural numbers (non-negative integers)
fact NonNegative {
  all t: Tumbler, i: t.comps.inds | t.comps[i] >= 0
}

-- Strict lexicographic less-than (same definition as T1).
-- k is 0-based. a < b iff some k >= 0 where:
--   (i)  k < min-length, a[0..k-1] = b[0..k-1], and a[k] < b[k]; or
--   (ii) k = len(a) < len(b)  -- a is a proper prefix of b
pred lexLT[a, b: Tumbler] {
  some k: Int | {
    k >= 0
    all i: Int | (i >= 0 and i < k) implies a.comps[i] = b.comps[i]
    (
      (k < #a.comps and k < #b.comps and a.comps[k] < b.comps[k])
      or
      (k = #a.comps and k < #b.comps)
    )
  }
}

-- ASSERTION 1 — BoundedWitness
-- When a < b, the witness k is bounded by both lengths:
--   k <= #a.comps  and  k <= #b.comps
-- i.e., k <= min(len(a), len(b)).
-- Verifies: no more than min(len(a), len(b)) component pairs are inspected.
assert BoundedWitness {
  all a, b: Tumbler | lexLT[a, b] implies
    some k: Int | {
      k >= 0
      k =< #a.comps
      k =< #b.comps
      all i: Int | (i >= 0 and i < k) implies a.comps[i] = b.comps[i]
      (
        (k < #a.comps and k < #b.comps and a.comps[k] < b.comps[k])
        or
        (k = #a.comps and k < #b.comps)
      )
    }
}

-- ASSERTION 2 — PrefixAgreementDetermines
-- If a and b agree on every common position (0 .. min-length - 1),
-- then order is decided by length alone — no deeper inspection needed.
-- Equivalently: a < b iff len(a) < len(b).
assert PrefixAgreementDetermines {
  all a, b: Tumbler |
    (all i: Int | (i >= 0 and i < #a.comps and i < #b.comps)
       implies a.comps[i] = b.comps[i])
    implies
    (lexLT[a, b] iff #a.comps < #b.comps)
}

-- ASSERTION 3 — Deterministic (Intrinsic)
-- If two pairs of tumblers share the same component sequences, they have the
-- same ordering.  No external data structure is consulted: the result is fully
-- determined by the content of the two sequences.
assert Deterministic {
  all a, b, c, d: Tumbler |
    (a.comps = c.comps and b.comps = d.comps) implies
    (lexLT[a, b] iff lexLT[c, d])
}

-- Non-vacuity: confirm the ordering relation is satisfiable
run NonVacuous {
  some a, b: Tumbler | lexLT[a, b]
} for 4 but exactly 2 Tumbler, 3 seq, 5 Int

check BoundedWitness            for 4 but 3 Tumbler, 3 seq, 5 Int
check PrefixAgreementDetermines for 4 but 3 Tumbler, 3 seq, 5 Int
check Deterministic             for 4 but 3 Tumbler, 3 seq, 5 Int
