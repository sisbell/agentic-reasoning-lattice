open util/integer

sig Tumbler {
    len: Int,
    comp: Int -> lone Int
} {
    len >= 1
    len =< 4
    all i: Int | (i >= 1 and i =< len) iff one comp[i]
    all i: Int | one comp[i] implies comp[i] >= 0
}

-- Maximum of two integers
fun maxOf[a, b: Int]: Int {
    a >= b => a else b
}

-- Zero-padded component access
fun zpad[t: Tumbler, i: Int]: Int {
    (i >= 1 and i =< t.len) => t.comp[i] else 0
}

-- k is the action point of w (least positive-component position)
pred isActionPoint[w: Tumbler, k: Int] {
    k >= 1
    k =< w.len
    w.comp[k] > 0
    all j: Int | (j >= 1 and j < k) implies w.comp[j] = 0
}

-- TumblerAdd: r = a + w with action point k
-- Prefix from a, advance at action point, tail from w
pred tumblerAdd[a, w, r: Tumbler, k: Int] {
    isActionPoint[w, k]
    k =< a.len
    r.len = w.len
    all i: Int | i >= 1 and i =< r.len implies
        (i < k implies r.comp[i] = a.comp[i]) and
        (i = k implies r.comp[i] = plus[a.comp[i], w.comp[i]]) and
        (i > k implies r.comp[i] = w.comp[i])
}

-- k is the zero-padded divergence of a and w
pred isZPD[a, w: Tumbler, k: Int] {
    k >= 1
    k =< maxOf[a.len, w.len]
    not (zpad[a, k] = zpad[w, k])
    all j: Int | (j >= 1 and j < k) implies zpad[a, j] = zpad[w, j]
}

-- No zero-padded divergence exists
pred noZPD[a, w: Tumbler] {
    all i: Int | (i >= 1 and i =< maxOf[a.len, w.len]) implies zpad[a, i] = zpad[w, i]
}

-- TumblerSub: s = a - w
-- Zero prefix, subtract at divergence, copy tail
pred tumblerSub[a, w, s: Tumbler] {
    s.len = maxOf[a.len, w.len]
    -- No divergence: result is zero tumbler
    noZPD[a, w] implies
        (all i: Int | i >= 1 and i =< s.len implies s.comp[i] = 0)
    -- Divergence at k: zero prefix, subtract at k, copy tail
    all k: Int | isZPD[a, w, k] implies
        (zpad[a, k] >= zpad[w, k] and
         (all i: Int | i >= 1 and i =< s.len implies
            (i < k implies s.comp[i] = 0) and
            (i = k implies s.comp[i] = minus[zpad[a, k], zpad[w, k]]) and
            (i > k implies s.comp[i] = zpad[a, i])))
}

-- Structural equality of tumblers
pred tumblerEq[a, b: Tumbler] {
    a.len = b.len
    all i: Int | i >= 1 and i =< a.len implies a.comp[i] = b.comp[i]
}

-- TA4: (a + w) - w = a under partial-inverse preconditions
assert PartialInverse {
    all a, w, r, s: Tumbler, k: Int |
        (isActionPoint[w, k]
         and k = a.len
         and w.len = k
         and (all i: Int | (i >= 1 and i < k) implies a.comp[i] = 0)
         and tumblerAdd[a, w, r, k]
         and tumblerSub[r, w, s])
        implies tumblerEq[s, a]
}

-- Non-vacuity: preconditions are satisfiable
run NonVacuity {
    some a, w, r, s: Tumbler, k: Int |
        isActionPoint[w, k]
        and k = a.len
        and w.len = k
        and (all i: Int | (i >= 1 and i < k) implies a.comp[i] = 0)
        and tumblerAdd[a, w, r, k]
        and tumblerSub[r, w, s]
} for 5 but exactly 4 Tumbler, 5 Int

check PartialInverse for 5 but exactly 4 Tumbler, 5 Int
