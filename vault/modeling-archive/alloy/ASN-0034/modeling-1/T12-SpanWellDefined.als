-- T12: SpanWellDefined — well-formed span implies non-emptiness
-- A span (s, l) with l > 0 and actionPt(l) <= #s gives s < s + l.

open util/integer

sig Tumbler {
  len: Int,
  comp: Int -> lone Int
} {
  len >= 1
  len =< 4
  all i: Int {
    (i >= 1 and i =< len) implies (one comp[i] and comp[i] >= 0 and comp[i] =< 7)
    (i < 1 or i > len) implies no comp[i]
  }
}

-- At least one nonzero component
pred positive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] != 0
}

-- First nonzero position
fun actionPt[w: Tumbler]: Int {
  min[{i: Int | i >= 1 and i =< w.len and w.comp[i] != 0}]
}

-- Tumbler strict ordering (T1)
pred tumblerLT[a, b: Tumbler] {
  -- Case (i): component divergence
  (some k: Int {
    k >= 1 and k =< a.len and k =< b.len
    a.comp[k] < b.comp[k]
    all j: Int | (j >= 1 and j < k) implies a.comp[j] = b.comp[j]
  })
  or
  -- Case (ii): proper prefix
  (a.len < b.len and
   all j: Int | (j >= 1 and j =< a.len) implies a.comp[j] = b.comp[j])
}

-- Tumbler addition: r = a + w (TA0)
pred tumblerAdd[a, w, r: Tumbler] {
  positive[w]
  let k = actionPt[w] {
    k =< a.len
    r.len = w.len
    all i: Int | (i >= 1 and i < k) implies r.comp[i] = a.comp[i]
    r.comp[k] = plus[a.comp[k], w.comp[k]]
    all i: Int | (i > k and i =< w.len) implies r.comp[i] = w.comp[i]
  }
}

-- Span well-formedness (T12)
pred spanWellFormed[s, l: Tumbler] {
  positive[l]
  actionPt[l] =< s.len
}

-- T12: well-formed span is non-empty (s < s + l)
assert SpanNonEmpty {
  all s, l, r: Tumbler |
    (spanWellFormed[s, l] and tumblerAdd[s, l, r])
    implies tumblerLT[s, r]
}

-- Non-vacuity
run FindSpan {
  some s, l, r: Tumbler |
    s != l and l != r and s != r and
    spanWellFormed[s, l] and tumblerAdd[s, l, r]
} for 5 but exactly 3 Tumbler, 5 Int

check SpanNonEmpty for 5 but exactly 3 Tumbler, 5 Int
