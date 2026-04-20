-- ASN-0034 D0: DisplacementWellDefined
-- Given a < b with divergence(a,b) <= #a, the displacement b - a is
-- well-defined, positive, with actionPoint = divergence and length = max(#a,#b).
-- The addition a + (b - a) is well-defined. When #a > #b the round-trip fails.

open util/integer

sig Tumbler {
  len: Int,
  val: Int -> lone Int
}

pred validTumbler[t: Tumbler] {
  t.len >= 1
  all i: Int {
    (i >= 1 and i =< t.len) implies (one t.val[i] and t.val[i] >= 0)
    (i < 1 or i > t.len) implies no t.val[i]
  }
}

fun zpad[t: Tumbler, i: Int]: Int {
  (some t.val[i]) implies t.val[i] else 0
}

fun minI[x, y: Int]: Int { x =< y implies x else y }
fun maxI[x, y: Int]: Int { x >= y implies x else y }

pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.val[i] > 0
}

pred isActionPoint[t: Tumbler, k: Int] {
  k >= 1 and k =< t.len
  t.val[k] > 0
  all i: Int | (i >= 1 and i < k) implies t.val[i] = 0
}

-- Divergence: first position where a and b differ
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

-- Tumbler ordering: a < b
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
pred tumblerEq[t1, t2: Tumbler] {
  t1.len = t2.len
  all i: Int | (i >= 1 and i =< t1.len) implies t1.val[i] = t2.val[i]
}

-- Subtraction: r = minuend (circled minus) subtrahend
pred isSub[minuend, subtrahend, r: Tumbler] {
  r.len = maxI[minuend.len, subtrahend.len]
  -- Frame: exactly one value at each in-range position, none outside
  all i: Int | (i < 1 or i > r.len) implies no r.val[i]
  all i: Int | (i >= 1 and i =< r.len) implies one r.val[i]
  -- Case split on zero-padded divergence
  {
    -- No zpd: padded sequences agree everywhere
    (all i: Int | (i >= 1 and i =< r.len) implies
        zpad[minuend, i] = zpad[subtrahend, i])
    all i: Int | (i >= 1 and i =< r.len) implies r.val[i] = 0
  }
  or
  {
    -- zpd at position k
    some k: Int {
      k >= 1 and k =< r.len
      not (zpad[minuend, k] = zpad[subtrahend, k])
      all i: Int | (i >= 1 and i < k) implies
        zpad[minuend, i] = zpad[subtrahend, i]
      zpad[minuend, k] >= zpad[subtrahend, k]
      all i: Int {
        (i >= 1 and i < k) implies r.val[i] = 0
        i = k implies r.val[i] = minus[zpad[minuend, k], zpad[subtrahend, k]]
        (i > k and i =< r.len) implies r.val[i] = zpad[minuend, i]
      }
    }
  }
}

-- Addition: r = base (circled plus) disp
pred isAdd[base, disp, r: Tumbler] {
  isPositive[disp]
  some k: Int {
    isActionPoint[disp, k]
    k =< base.len
    r.len = disp.len
    -- Frame
    all i: Int | (i < 1 or i > r.len) implies no r.val[i]
    all i: Int | (i >= 1 and i =< r.len) implies one r.val[i]
    -- Components
    all i: Int {
      (i >= 1 and i < k) implies r.val[i] = base.val[i]
      i = k implies r.val[i] = plus[base.val[k], disp.val[k]]
      (i > k and i =< r.len) implies r.val[i] = disp.val[i]
    }
  }
}

-- Postconditions 1-4: subtraction yields valid positive tumbler
-- with action point = divergence, length = max
assert D0_Sub {
  all a, b, w: Tumbler, k: Int |
    (validTumbler[a] and validTumbler[b]
     and tumblerLt[a, b]
     and isDivergence[a, b, k] and k =< a.len
     and isSub[b, a, w])
    implies
    (validTumbler[w] and isPositive[w]
     and isActionPoint[w, k]
     and w.len = maxI[a.len, b.len])
}

-- Postcondition 5: addition result is valid
assert D0_Add {
  all a, b, w, r: Tumbler, k: Int |
    (validTumbler[a] and validTumbler[b]
     and tumblerLt[a, b]
     and isDivergence[a, b, k] and k =< a.len
     and isSub[b, a, w] and isAdd[a, w, r])
    implies
    validTumbler[r]
}

-- Postcondition 6: round-trip fails when #a > #b
assert D0_NoRoundTrip {
  all a, b, w, r: Tumbler, k: Int |
    (validTumbler[a] and validTumbler[b]
     and tumblerLt[a, b]
     and isDivergence[a, b, k] and k =< a.len
     and isSub[b, a, w] and isAdd[a, w, r]
     and a.len > b.len)
    implies
    not tumblerEq[r, b]
}

-- Non-vacuity: full pipeline is satisfiable
run NonVacuity {
  some disj a, b, w, r: Tumbler, k: Int {
    validTumbler[a] and validTumbler[b]
    tumblerLt[a, b]
    isDivergence[a, b, k]
    k =< a.len
    isSub[b, a, w]
    isAdd[a, w, r]
  }
} for 5 but exactly 4 Tumbler, 5 Int

check D0_Sub for 5 but exactly 3 Tumbler, 5 Int
check D0_Add for 5 but exactly 4 Tumbler, 5 Int
check D0_NoRoundTrip for 5 but exactly 4 Tumbler, 5 Int
