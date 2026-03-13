open util/integer

-- Tumbler: variable-length sequence of natural number components
sig Tumbler {
  len: Int,
  val: Int -> lone Int
} {
  len >= 1
  len =< 4
  all i: Int | (i >= 1 and i =< len) iff one val[i]
  all i: Int | some val[i] implies val[i] >= 0
  all i: Int | some val[i] implies val[i] =< 7
}

-- A tumbler is positive iff it has at least one nonzero component
pred positive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.val[i] > 0
}

-- Action point: index of first nonzero component
fun actionPoint[t: Tumbler]: Int {
  min[{i: Int | i >= 1 and i =< t.len and t.val[i] > 0}]
}

-- Zero-padded component lookup
fun padComp[t: Tumbler, i: Int]: Int {
  (i >= 1 and i =< t.len) implies t.val[i] else 0
}

-- Tumbler addition: result = a ⊕ w
pred tumblerAdd[a, w, result: Tumbler] {
  positive[w]
  let k = actionPoint[w] {
    k =< a.len
    result.len = w.len
    all i: Int | i >= 1 and i =< result.len implies {
      i < k implies result.val[i] = a.val[i]
      i = k implies result.val[i] = plus[a.val[k], w.val[k]]
      i > k implies result.val[i] = w.val[i]
    }
  }
}

-- Tumbler subtraction: result = endPos ⊖ w
pred tumblerSub[endPos, w, result: Tumbler] {
  let ml = (endPos.len >= w.len implies endPos.len else w.len),
      diffSet = {i: Int | i >= 1 and i =< ml and
                  not (padComp[endPos, i] = padComp[w, i])} {
    result.len = ml
    -- No divergence: endPos = w after padding, result is zero tumbler
    (no diffSet) implies
      (all i: Int | i >= 1 and i =< ml implies result.val[i] = 0)
    -- Divergence exists
    (some diffSet) implies
      (let k = min[diffSet] {
        padComp[endPos, k] >= padComp[w, k]
        all i: Int | i >= 1 and i =< ml implies {
          i < k implies result.val[i] = 0
          i = k implies result.val[i] = minus[padComp[endPos, k], padComp[w, k]]
          i > k implies result.val[i] = padComp[endPos, i]
        }
      })
  }
}

-- Structural equality of two tumblers
pred tumblerEqual[a, b: Tumbler] {
  a.len = b.len
  all i: Int | i >= 1 and i =< a.len implies a.val[i] = b.val[i]
}

-- TA4 precondition: action point at last position of a,
-- w has same length, a is zero before the action point
pred ta4Pre[a, w: Tumbler] {
  positive[w]
  let k = actionPoint[w] {
    k = a.len
    w.len = k
    all i: Int | i >= 1 and i < k implies a.val[i] = 0
  }
}

-- TA4: (a ⊕ w) ⊖ w = a under TA4 preconditions
assert TA4_PartialInverse {
  all a, w, s, r: Tumbler |
    (ta4Pre[a, w] and tumblerAdd[a, w, s] and tumblerSub[s, w, r])
    implies tumblerEqual[r, a]
}

-- Non-vacuity: the preconditions are satisfiable
run NonVacuity {
  some a, w, s, r: Tumbler |
    ta4Pre[a, w] and tumblerAdd[a, w, s] and tumblerSub[s, w, r]
} for 5 but exactly 4 Tumbler, 5 Int

check TA4_PartialInverse for 5 but exactly 4 Tumbler, 5 Int
