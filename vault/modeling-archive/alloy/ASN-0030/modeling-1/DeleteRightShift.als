-- ASN-0030 A4(e) — DeleteRightShift
-- After DELETE(d, p, k), positions p+k..n_d shift left by k:
--   (A j : p + k ≤ j ≤ n_d : Σ'.V(d)(j − k) = Σ.V(d)(j))
-- Assert: right shift produces a well-formed contiguous V-list
-- and new length equals n_d - k.

open util/integer

sig Addr {}
sig Document {}

sig State {
  docs: set Document,
  vmap: Document -> Int -> lone Addr
} {
  -- V-map entries only for active documents
  (vmap.Addr).Int in docs
  -- Positions are positive
  all d: docs, j: Int | some d.vmap[j] implies j >= 1
}

-- Document length: count of occupied positions
fun docLen[s: State, d: Document]: Int {
  #{j: Int | some d.(s.vmap)[j]}
}

-- V-list is contiguous: exactly positions 1..n are occupied
pred wellFormed[s: State, d: Document] {
  d in s.docs
  let n = docLen[s, d] |
    all j: Int | some d.(s.vmap)[j] iff (j >= 1 and j =< n)
}

-- DELETE precondition
pred DeletePre[s: State, d: Document, p, k: Int] {
  wellFormed[s, d]
  p >= 1
  k >= 1
  let last = plus[p, minus[k, 1]] {
    last >= p                          -- overflow guard
    last =< docLen[s, d]
  }
}

-- DELETE operation: left frame + right shift + cleanup
pred Delete[s, s2: State, d: Document, p, k: Int] {
  DeletePre[s, d, p, k]
  let n = docLen[s, d] {
    -- A4(d): left frame — positions before p unchanged
    all j: Int | (j >= 1 and j < p) implies
      d.(s2.vmap)[j] = d.(s.vmap)[j]
    -- A4(e): right shift — positions p+k..n shift left by k
    all j: Int | (j >= plus[p, k] and j =< n) implies
      d.(s2.vmap)[minus[j, k]] = d.(s.vmap)[j]
    -- nothing beyond new length
    all j: Int | (j < 1 or j > minus[n, k]) implies
      no d.(s2.vmap)[j]
  }
  -- frame: other documents unchanged
  all d2: s.docs - d | d2.(s2.vmap) = d2.(s.vmap)
  s2.docs = s.docs
}

-- Post-state is well-formed: right shift produces contiguous V-list
assert DeletePostWellFormed {
  all s, s2: State, d: Document, p, k: Int |
    Delete[s, s2, d, p, k] implies wellFormed[s2, d]
}

-- Post-state length is n_d - k
assert DeleteNewLength {
  all s, s2: State, d: Document, p, k: Int |
    Delete[s, s2, d, p, k] implies
      docLen[s2, d] = minus[docLen[s, d], k]
}

-- Non-vacuity: a valid delete exists
run FindDelete {
  some s, s2: State, d: Document, p, k: Int |
    Delete[s, s2, d, p, k]
} for 4 but exactly 2 State, 6 Int

check DeletePostWellFormed for 5 but exactly 2 State, 6 Int
check DeleteNewLength for 5 but exactly 2 State, 6 Int
