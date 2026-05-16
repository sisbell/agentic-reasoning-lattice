-- TA1-strict (StrictOrderPreservation) — ASN-0034
-- (A a, b, w : a < b, w > 0, actionPoint(w) >= divergence(a,b),
--              actionPoint(w) =< min(#a, #b) : a + w < b + w)

open util/integer

sig Tumbler {
  components: seq Int
}

-- All tumblers are non-empty with non-negative components
fact TumblerWF {
  all t: Tumbler {
    some t.components
    all i: t.components.inds | t.components[i] >= 0
  }
}

-- Minimum of two integers
fun intMin[x, y: Int]: Int {
  (x =< y) => x else y
}

-- T1 tumbler strict ordering (0-based indices)
-- Case (i): first shared position where they differ, a's component is smaller
-- Case (ii): a is a proper prefix of b
pred tumblerLt[a, b: Tumbler] {
  some d: Int {
    d >= 0
    -- All shared positions before d agree
    all i: Int | (i >= 0 and i < d and i < #a.components and i < #b.components)
      implies a.components[i] = b.components[i]
    {
      -- Case (i): within-range disagreement with a smaller
      (d < #a.components and d < #b.components
        and a.components[d] < b.components[d])
      or
      -- Case (ii): a is a proper prefix of b
      (d = #a.components and #a.components < #b.components)
    }
  }
}

-- Positive tumbler: at least one non-zero component
pred positive[t: Tumbler] {
  some i: t.components.inds | t.components[i] > 0
}

-- Action point (0-based): first non-zero index in displacement
pred hasActionPoint[w: Tumbler, k: Int] {
  k >= 0
  k < #w.components
  w.components[k] > 0
  all i: Int | (i >= 0 and i < k) implies w.components[i] = 0
}

-- Divergence point (0-based)
-- Case (i): first index in shared range where a and b differ
-- Case (ii): min(len(a), len(b)) when one is a proper prefix of the other
pred hasDivergence[a, b: Tumbler, d: Int] {
  let ml = intMin[#a.components, #b.components] | {
    d >= 0
    d =< ml
    -- All shared positions before d agree
    all i: Int | (i >= 0 and i < d and i < ml)
      implies a.components[i] = b.components[i]
    -- At d: either they differ (case i) or prefix boundary (case ii)
    (d < ml) implies not (a.components[d] = b.components[d])
    (d = ml) implies not (#a.components = #b.components)
  }
}

-- Tumbler addition: result = a ⊕ w with action point k (0-based)
-- Prefix from a, add at k, tail from w
pred tumblerAdd[a, w, result: Tumbler, k: Int] {
  hasActionPoint[w, k]
  k < #a.components
  -- Result has same length as displacement
  #result.components = #w.components
  -- Prefix: copy from a
  all i: Int | (i >= 0 and i < k)
    implies result.components[i] = a.components[i]
  -- Action point: add components
  result.components[k] = plus[a.components[k], w.components[k]]
  -- Tail: copy from displacement
  all i: Int | (i > k and i < #w.components)
    implies result.components[i] = w.components[i]
}

-- TA1-strict assertion: tumbler addition preserves strict order
-- when action point falls at or beyond the divergence
assert StrictOrderPreservation {
  all a, b, w, aw, bw: Tumbler, k, d: Int |
    (tumblerLt[a, b] and positive[w] and
     hasActionPoint[w, k] and hasDivergence[a, b, d] and
     k < intMin[#a.components, #b.components] and
     k >= d and
     tumblerAdd[a, w, aw, k] and tumblerAdd[b, w, bw, k])
    implies tumblerLt[aw, bw]
}

-- Non-vacuity: the preconditions are satisfiable
run NonVacuity {
  some a, b, w, aw, bw: Tumbler, k, d: Int |
    tumblerLt[a, b] and positive[w] and
    hasActionPoint[w, k] and hasDivergence[a, b, d] and
    k < intMin[#a.components, #b.components] and
    k >= d and
    tumblerAdd[a, w, aw, k] and tumblerAdd[b, w, bw, k]
} for 5 but exactly 5 Tumbler, 3 seq, 5 Int

check StrictOrderPreservation for 5 but exactly 5 Tumbler, 3 seq, 5 Int
