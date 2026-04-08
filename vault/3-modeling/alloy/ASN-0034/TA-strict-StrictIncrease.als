open util/integer

sig Tumbler {
  len: Int,
  val: Int -> lone Int
} {
  len >= 1
  all i: Int | (i >= 1 and i =< len) iff one val[i]
  all i: Int | one val[i] implies val[i] >= 0
}

-- minimum of two integers
fun min2[a, b: Int]: Int {
  (a =< b) => a else b
}

-- T1 tumbler strict ordering (lexicographic with length extension)
pred tumblerLT[a, b: Tumbler] {
  -- Case (i): divergence within common prefix length
  (some k: Int {
    k >= 1
    k =< min2[a.len, b.len]
    all i: Int | (i >= 1 and i < k) implies a.val[i] = b.val[i]
    a.val[k] < b.val[k]
  })
  or
  -- Case (ii): full prefix match, shorter tumbler is less
  ((all i: Int | (i >= 1 and i =< min2[a.len, b.len]) implies a.val[i] = b.val[i])
    and a.len < b.len)
}

pred tumblerGT[a, b: Tumbler] {
  tumblerLT[b, a]
}

-- w > 0: at least one component is positive
pred isPositive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.val[i] > 0
}

-- action point: first positive position
fun actionPoint[w: Tumbler]: lone Int {
  {i: Int | i >= 1 and i =< w.len and w.val[i] > 0 and
    (all j: Int | (j >= 1 and j < i) implies w.val[j] = 0)}
}

-- TA0: r = a ⊕ w (tumbler addition)
pred tumblerAdd[a, w, r: Tumbler] {
  isPositive[w]
  let k = actionPoint[w] {
    -- precondition: action point within a's length
    k =< a.len
    -- result length equals displacement length
    r.len = w.len
    -- prefix copy: r_i = a_i for i < k
    all i: Int | (i >= 1 and i < k) implies r.val[i] = a.val[i]
    -- action point: r_k = a_k + w_k
    r.val[k] = plus[a.val[k], w.val[k]]
    -- tail copy: r_i = w_i for i > k
    all i: Int | (i > k and i =< w.len) implies r.val[i] = w.val[i]
  }
}

-- TA-strict: adding a positive displacement strictly increases position
assert StrictIncrease {
  all a, w, r: Tumbler |
    tumblerAdd[a, w, r] implies tumblerGT[r, a]
}

-- non-vacuity: a valid addition exists
run NonVacuity {
  some a, w, r: Tumbler |
    a != w and w != r and a != r and
    tumblerAdd[a, w, r]
} for 5 but exactly 3 Tumbler, 5 Int

check StrictIncrease for 5 but exactly 3 Tumbler, 5 Int
