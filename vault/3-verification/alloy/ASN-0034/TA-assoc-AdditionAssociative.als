-- TA-assoc (AdditionAssociative)
-- (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) when both compositions are well-defined

open util/integer

sig Tumbler {
  comp: Int -> lone Int,
  len: one Int
}

fact TumblerWF {
  all t: Tumbler {
    t.len >= 1
    t.len =< 3
    all i: Int {
      (i >= 1 and i =< t.len) implies one t.comp[i]
      (i < 1 or i > t.len) implies no t.comp[i]
    }
    all i: Int | some t.comp[i] implies t.comp[i] >= 0
  }
}

pred positive[t: Tumbler] {
  some i: Int | i >= 1 and i =< t.len and t.comp[i] > 0
}

pred isActionPoint[t: Tumbler, k: Int] {
  k >= 1
  k =< t.len
  t.comp[k] > 0
  all j: Int | (j >= 1 and j < k) implies t.comp[j] = 0
}

-- TumblerAdd: result = a ⊕ w (constructive definition)
-- Precondition: w > 0, actionPoint(w) <= #a
-- Definition: r[i] = a[i] for i < k; r[k] = a[k] + w[k]; r[i] = w[i] for i > k
-- Postcondition: #(a ⊕ w) = #w
pred tumblerAdd[a, w, result: Tumbler] {
  positive[w]
  some k: Int {
    isActionPoint[w, k]
    k =< a.len
    result.len = w.len
    all i: Int | (i >= 1 and i < k) implies result.comp[i] = a.comp[i]
    result.comp[k] = plus[a.comp[k], w.comp[k]]
    all i: Int | (i > k and i =< w.len) implies result.comp[i] = w.comp[i]
  }
}

-- Postcondition 1: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c)
assert AdditionAssociative {
  all a, b, c, ab, abc_l, bc, abc_r: Tumbler |
    (positive[b] and positive[c] and
     tumblerAdd[a, b, ab] and
     tumblerAdd[ab, c, abc_l] and
     tumblerAdd[b, c, bc] and
     tumblerAdd[a, bc, abc_r])
    implies
    (abc_l.len = abc_r.len and
     (all i: Int | (i >= 1 and i =< abc_l.len) implies
       abc_l.comp[i] = abc_r.comp[i]))
}

-- Postcondition 2: #((a ⊕ b) ⊕ c) = #(a ⊕ (b ⊕ c)) = #c
assert ResultLengthIsC {
  all a, b, c, ab, abc_l, bc, abc_r: Tumbler |
    (positive[b] and positive[c] and
     tumblerAdd[a, b, ab] and
     tumblerAdd[ab, c, abc_l] and
     tumblerAdd[b, c, bc] and
     tumblerAdd[a, bc, abc_r])
    implies
    (abc_l.len = c.len and abc_r.len = c.len)
}

-- Postcondition 3: actionPoint(b ⊕ c) = min(k_b, k_c)
assert BCSumActionPoint {
  all b, c, bc: Tumbler, kb, kc, kbc: Int |
    (positive[b] and positive[c] and
     tumblerAdd[b, c, bc] and
     isActionPoint[b, kb] and
     isActionPoint[c, kc] and
     isActionPoint[bc, kbc])
    implies
    ((kb =< kc implies kbc = kb) and
     (kc < kb implies kbc = kc))
}

-- Non-vacuity: the full associative composition is satisfiable
run NonVacuity {
  some disj a, b, c, ab, abc_l, bc, abc_r: Tumbler |
    positive[b] and positive[c] and
    tumblerAdd[a, b, ab] and
    tumblerAdd[ab, c, abc_l] and
    tumblerAdd[b, c, bc] and
    tumblerAdd[a, bc, abc_r]
} for 7 but 5 Int

check AdditionAssociative for 7 but 5 Int
check ResultLengthIsC for 7 but 5 Int
check BCSumActionPoint for 7 but 5 Int
