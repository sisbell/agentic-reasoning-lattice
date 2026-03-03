-- TA1: WeakOrderPreservation
-- (A a, b, w : a < b ∧ w > 0 ∧ k ≤ min(#a,#b) : a ⊕ w ≤ b ⊕ w)
-- k is the action point of w (1-indexed in spec; 0-indexed in this model).
-- Precondition k ≤ min(#a,#b) becomes ap[w] in a.inds and ap[w] in b.inds.
--
-- Tumblers modeled as seq Int with non-negative components.
-- Ordering is lexicographic with zero-extension for differing lengths.

-- Component with zero-extension for out-of-bounds positions
fun comp[t: seq Int, i: Int]: Int {
  i in t.inds implies t[i] else 0
}

-- Well-formed tumbler: all components non-negative
pred wf[t: seq Int] {
  all i: t.inds | t[i] >= 0
}

-- Positive tumbler: at least one nonzero component
pred isPos[w: seq Int] {
  some i: w.inds | not (w[i] = 0)
}

-- Action point: 0-indexed position of first nonzero component
fun ap[w: seq Int]: Int {
  min[{i: w.inds | not (w[i] = 0)}]
}

-- Lexicographic strict less-than with zero-extension
pred tLt[a, b: seq Int] {
  some i: Int | {
    i >= 0
    comp[a, i] < comp[b, i]
    all j: Int | (j >= 0 and j < i) implies comp[a, j] = comp[b, j]
  }
}

-- Lexicographic less-than-or-equal
pred tLe[a, b: seq Int] {
  not tLt[b, a]
}

-- TumblerAdd: r = a ⊕ w
-- Pre: isPos[w], ap[w] in a.inds
-- Result length equals #w; copies a before the action point,
-- adds at the action point, copies w after the action point.
pred tAdd[a, w, r: seq Int] {
  let k = ap[w] | {
    #r = #w
    all i: w.inds | {
      (i < k) implies r[i] = a[i]
      (i = k) implies r[i] = plus[a[i], w[i]]
      (i > k) implies r[i] = w[i]
    }
  }
}

-- TA1: Adding a positive displacement preserves weak order
assert WeakOrderPreservation {
  all a, b, w, ra, rb: seq Int | {
    wf[a] and wf[b] and wf[w]
    isPos[w]
    tLt[a, b]
    ap[w] in a.inds
    ap[w] in b.inds
    tAdd[a, w, ra]
    tAdd[b, w, rb]
  } implies tLe[ra, rb]
}

check WeakOrderPreservation for 4 but 4 seq, 5 Int

-- Non-vacuity: the precondition is satisfiable
run NonVacuous {
  some a, b, w, ra, rb: seq Int | {
    wf[a] and wf[b] and wf[w]
    isPos[w]
    tLt[a, b]
    ap[w] in a.inds
    ap[w] in b.inds
    tAdd[a, w, ra]
    tAdd[b, w, rb]
  }
} for 4 but 4 seq, 5 Int
