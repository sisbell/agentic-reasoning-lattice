-- T12 SpanWellDefinedness
-- A well-formed span (s, l) with l > 0 and actionPoint(l) <= #s satisfies:
-- (a) s ⊕ l ∈ T (endpoint valid)
-- (b) s ∈ span(s, l) (non-empty, by TA-strict)
-- (c) span(s, l) is order-convex under T1

open util/integer

sig Tumbler {
  len: Int,
  val: Int -> lone Int
}

pred validTumbler[t: Tumbler] {
  t.len >= 1
  t.len =< 3
  all i: Int {
    (i >= 1 and i =< t.len) implies (one t.val[i] and t.val[i] >= 0)
    (i < 1 or i > t.len) implies no t.val[i]
  }
}

fact AllValid { all t: Tumbler | validTumbler[t] }

fun minI[x, y: Int]: Int { x =< y implies x else y }

pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.val[i] > 0
}

pred isActionPoint[t: Tumbler, k: Int] {
  k >= 1 and k =< t.len
  t.val[k] > 0
  all i: Int | (i >= 1 and i < k) implies t.val[i] = 0
}

-- T1 lexicographic divergence
pred isDivergence[a, b: Tumbler, k: Int] {
  let ml = minI[a.len, b.len] {
    -- Case (i): mismatch within shared length
    (k >= 1 and k =< ml
     and not (a.val[k] = b.val[k])
     and (all i: Int | (i >= 1 and i < k) implies a.val[i] = b.val[i]))
    or
    -- Case (ii): prefix match, lengths differ
    (k = plus[ml, 1] and not (a.len = b.len)
     and (all i: Int | (i >= 1 and i =< ml) implies a.val[i] = b.val[i]))
  }
}

-- T1 lexicographic strict less-than
pred tumblerLt[a, b: Tumbler] {
  some k: Int {
    isDivergence[a, b, k]
    let ml = minI[a.len, b.len] {
      k =< ml implies a.val[k] < b.val[k]
      k = plus[ml, 1] implies a.len < b.len
    }
  }
}

-- Sequence equality
pred tumblerEq[a, b: Tumbler] {
  a.len = b.len
  all i: Int | (i >= 1 and i =< a.len) implies a.val[i] = b.val[i]
}

-- Less-than-or-equal
pred tumblerLe[a, b: Tumbler] {
  tumblerLt[a, b] or tumblerEq[a, b]
}

-- TA0: displacement addition r = s ⊕ l
pred isAdd[s, l, r: Tumbler] {
  isPositive[l]
  some k: Int {
    isActionPoint[l, k]
    k =< s.len
    r.len = l.len
    all i: Int {
      (i >= 1 and i < k) implies r.val[i] = s.val[i]
      i = k implies r.val[i] = plus[s.val[k], l.val[k]]
      (i > k and i =< r.len) implies r.val[i] = l.val[i]
    }
  }
}

-- Span membership: s ≤ t < endpoint
pred inSpan[t, s, endpoint: Tumbler] {
  tumblerLe[s, t]
  tumblerLt[t, endpoint]
}

-- Span configuration
one sig SpanCfg {
  s: one Tumbler,
  l: one Tumbler,
  e: one Tumbler
}

fact SpanPreconditions {
  isAdd[SpanCfg.s, SpanCfg.l, SpanCfg.e]
}

-- (a) Endpoint exists in T (is a valid tumbler)
assert EndpointValid {
  validTumbler[SpanCfg.e]
}

-- (b) s ∈ span(s, l): start is in the span
assert SpanNonEmpty {
  inSpan[SpanCfg.s, SpanCfg.s, SpanCfg.e]
}

-- (c) span(s, l) is order-convex: a,c in span and a ≤ b ≤ c implies b in span
assert SpanConvex {
  all a, b, c: Tumbler |
    (inSpan[a, SpanCfg.s, SpanCfg.e]
     and inSpan[c, SpanCfg.s, SpanCfg.e]
     and tumblerLe[a, b] and tumblerLe[b, c])
    implies
    inSpan[b, SpanCfg.s, SpanCfg.e]
}

-- Non-vacuity: a valid span configuration with a member exists
run NonVacuous {
  some t: Tumbler | inSpan[t, SpanCfg.s, SpanCfg.e]
} for 4 but exactly 4 Tumbler, 4 Int

check EndpointValid for 4 but exactly 4 Tumbler, 4 Int
check SpanNonEmpty for 4 but exactly 4 Tumbler, 4 Int
check SpanConvex for 4 but exactly 4 Tumbler, 4 Int
