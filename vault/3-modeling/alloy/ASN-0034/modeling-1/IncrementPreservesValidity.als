open util/ordering[Pos]

sig Pos {}

sig Tumbler {
  elems: set Pos,
  zeroAt: set Pos
} {
  zeroAt in elems
  -- elems forms a contiguous prefix of the position ordering
  all p, q: Pos | p in elems and lt[q, p] implies q in elems
  some elems
}

-- Last position in a tumbler's element sequence
fun lastElem[t: Tumbler]: Pos {
  {p: t.elems | no (p.next & t.elems)}
}

-- T4: valid tumbler structure
-- Non-empty fields (no adjacent zeros, first/last nonzero), at most 4 fields
pred T4[t: Tumbler] {
  -- no adjacent zeros
  no p: t.zeroAt | p.next in t.zeroAt
  -- first component nonzero
  first not in t.zeroAt
  -- last component nonzero
  lastElem[t] not in t.zeroAt
  -- at most 3 zero separators
  #t.zeroAt =< 3
}

-- TA5: increment at level k — append (k-1) zeros then one nonzero
pred Increment[t, tPost: Tumbler, k: Int] {
  k >= 0
  k = 0 implies {
    tPost.elems = t.elems
    tPost.zeroAt = t.zeroAt
  }
  k >= 1 implies {
    t.elems in tPost.elems
    let newPos = tPost.elems - t.elems {
      #newPos = k
      -- preserve zero status of original positions
      all p: t.elems | (p in t.zeroAt) iff (p in tPost.zeroAt)
      -- last new position is nonzero (child value); all others are zero separators
      let lastNew = {p: newPos | no (p.next & newPos)} {
        one lastNew
        lastNew not in tPost.zeroAt
        (newPos - lastNew) in tPost.zeroAt
      }
    }
  }
}

-- TA5 preserves T4 for k <= 2 with zeros(t) + (k-1) <= 3
assert IncrementPreservesT4 {
  all t, tPost: Tumbler, k: Int |
    (T4[t] and k >= 0 and k =< 2 and
     Increment[t, tPost, k] and
     (k = 0 or plus[#t.zeroAt, minus[k, 1]] =< 3))
    implies T4[tPost]
}

-- TA5 violates T4 for k >= 3 (adjacent zeros in appended sequence)
assert IncrementViolatesT4ForLargeK {
  all t, tPost: Tumbler, k: Int |
    (T4[t] and k >= 3 and Increment[t, tPost, k])
    implies not T4[tPost]
}

run NonVacuity {
  some t, tPost: Tumbler |
    T4[t] and Increment[t, tPost, 2] and T4[tPost]
} for 7 but exactly 2 Tumbler

check IncrementPreservesT4 for 7 but exactly 2 Tumbler
check IncrementViolatesT4ForLargeK for 7 but exactly 2 Tumbler
