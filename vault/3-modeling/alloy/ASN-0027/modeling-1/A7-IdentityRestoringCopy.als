open util/integer

sig Addr {}
sig Doc {}

sig State {
  content: Doc -> Int -> lone Addr,
  len: Doc -> one Int
}

pred validState[s: State] {
  all d: Doc {
    s.len[d] >= 0
    all i: Int {
      (i >= 0 and i < s.len[d]) implies one s.content[d][i]
      (i < 0 or i >= s.len[d]) implies no s.content[d][i]
    }
  }
}

-- DELETE(s0, d, p, k) = s1
-- Removes k elements starting at position p from document d.
-- Positions after the deleted span shift down by k.
pred Delete[s0, s1: State, d: Doc, p, k: Int] {
  p >= 0
  k > 0
  plus[p, k] =< s0.len[d]

  s1.len[d] = minus[s0.len[d], k]

  -- positions before p: unchanged
  all i: Int | (i >= 0 and i < p) implies
    s1.content[d][i] = s0.content[d][i]

  -- positions at and after p: shifted down by k
  all i: Int | (i >= p and i < s1.len[d]) implies
    s1.content[d][i] = s0.content[d][plus[i, k]]

  -- nothing beyond new length
  all i: Int | (i < 0 or i >= s1.len[d]) implies
    no s1.content[d][i]

  -- other documents unchanged
  all d2: Doc - d {
    s1.len[d2] = s0.len[d2]
    all i: Int | s1.content[d2][i] = s0.content[d2][i]
  }
}

-- COPY(dSrc, (q, k), dDst, p) in state s0, producing s1
-- Inserts k elements from dSrc[q..q+k-1] into dDst at position p.
-- Existing elements at p and beyond shift up by k.
pred Copy[s0, s1: State, dSrc: Doc, q, k: Int, dDst: Doc, p: Int] {
  q >= 0
  k > 0
  p >= 0
  plus[q, k] =< s0.len[dSrc]
  p =< s0.len[dDst]

  s1.len[dDst] = plus[s0.len[dDst], k]

  -- positions before p: unchanged
  all i: Int | (i >= 0 and i < p) implies
    s1.content[dDst][i] = s0.content[dDst][i]

  -- copied span: dDst[p..p+k-1] = dSrc[q..q+k-1]
  all j: Int | (j >= 0 and j < k) implies
    s1.content[dDst][plus[p, j]] = s0.content[dSrc][plus[q, j]]

  -- positions after insertion: shifted up by k
  all i: Int | (i >= p and i < s0.len[dDst]) implies
    s1.content[dDst][plus[i, k]] = s0.content[dDst][i]

  -- nothing beyond new length
  all i: Int | (i < 0 or i >= s1.len[dDst]) implies
    no s1.content[dDst][i]

  -- other documents unchanged
  all d2: Doc - dDst {
    s1.len[d2] = s0.len[d2]
    all i: Int | s1.content[d2][i] = s0.content[d2][i]
  }
}

-- A7: IdentityRestoringCopy
-- DELETE removes addresses a_j from d[p..p+k-1].
-- If d' still holds those addresses at q..q+k-1 in the post-DELETE state,
-- then COPY(d', (q,k), d, p) restores d[p+j] = a_j for all j in 0..k-1.
assert IdentityRestoringCopy {
  all s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
    (validState[s0] and
     Delete[s0, s1, d, p, k] and
     q >= 0 and
     plus[q, k] =< s1.len[dPrime] and
     (all j: Int | (j >= 0 and j < k) implies
       s1.content[dPrime][plus[q, j]] = s0.content[d][plus[p, j]]) and
     Copy[s1, s2, dPrime, q, k, d, p])
    implies
     (all j: Int | (j >= 0 and j < k) implies
       s2.content[d][plus[p, j]] = s0.content[d][plus[p, j]])
}

check IdentityRestoringCopy for 4 but exactly 3 State, 5 Int

run NonVacuity {
  some s0, s1, s2: State, d, dPrime: Doc, p, q, k: Int |
    validState[s0] and
    Delete[s0, s1, d, p, k] and
    q >= 0 and
    plus[q, k] =< s1.len[dPrime] and
    (all j: Int | (j >= 0 and j < k) implies
      s1.content[dPrime][plus[q, j]] = s0.content[d][plus[p, j]]) and
    Copy[s1, s2, dPrime, q, k, d, p]
} for 4 but exactly 3 State, 5 Int
