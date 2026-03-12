-- ASN-0030 A5(e) — CopyRightShift
-- After COPY(d_s, p_s, k, d_t, p_t), existing target entries shift right:
--   (A j : p_t ≤ j ≤ n_{d_t} : Σ'.V(d_t)(j + k) = Σ.V(d_t)(j))
-- Assert: right shift produces a well-formed contiguous V-list
-- and new length equals n_{d_t} + k.

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

-- COPY precondition
pred CopyPre[s: State, ds, dt: Document, ps, k, pt: Int] {
  ds in s.docs
  dt in s.docs
  k >= 1
  ps >= 1
  let srcEnd = plus[ps, minus[k, 1]] {
    srcEnd >= ps                          -- overflow guard
    srcEnd =< docLen[s, ds]
  }
  pt >= 1
  pt =< plus[docLen[s, dt], 1]
}

-- COPY operation: left frame + source insert + right shift + cleanup
pred Copy[s, s2: State, ds, dt: Document, ps, k, pt: Int] {
  CopyPre[s, ds, dt, ps, k, pt]
  let ndt = docLen[s, dt] {
    -- A5(d): left frame — positions before p_t unchanged
    all j: Int | (j >= 1 and j < pt) implies
      dt.(s2.vmap)[j] = dt.(s.vmap)[j]
    -- A5(e): right shift — positions p_t..n_dt shift right by k
    all j: Int | (j >= pt and j =< ndt) implies
      dt.(s2.vmap)[plus[j, k]] = dt.(s.vmap)[j]
    -- A5(b): gap filled from source
    all j: Int | (j >= 0 and j < k) implies
      dt.(s2.vmap)[plus[pt, j]] = ds.(s.vmap)[plus[ps, j]]
    -- nothing beyond new length
    all j: Int | (j < 1 or j > plus[ndt, k]) implies
      no dt.(s2.vmap)[j]
  }
  -- frame: other documents unchanged
  all d2: s.docs - dt | d2.(s2.vmap) = d2.(s.vmap)
  s2.docs = s.docs
}

-- Post-state is well-formed: right shift produces contiguous V-list
assert CopyPostWellFormed {
  all s, s2: State, ds, dt: Document, ps, k, pt: Int |
    (wellFormed[s, ds] and wellFormed[s, dt] and Copy[s, s2, ds, dt, ps, k, pt])
      implies wellFormed[s2, dt]
}

-- Post-state target length is n_dt + k
assert CopyNewLength {
  all s, s2: State, ds, dt: Document, ps, k, pt: Int |
    (wellFormed[s, ds] and wellFormed[s, dt] and Copy[s, s2, ds, dt, ps, k, pt])
      implies docLen[s2, dt] = plus[docLen[s, dt], k]
}

-- Shifted entries preserve their values
assert ShiftPreservesValues {
  all s, s2: State, ds, dt: Document, ps, k, pt: Int |
    (wellFormed[s, dt] and Copy[s, s2, ds, dt, ps, k, pt]) implies
    (all j: Int | (j >= pt and j =< docLen[s, dt]) implies
      some dt.(s2.vmap)[plus[j, k]])
}

-- Non-vacuity: a valid copy exists
run FindCopy {
  some s, s2: State, ds, dt: Document, ps, k, pt: Int |
    wellFormed[s, ds] and wellFormed[s, dt] and Copy[s, s2, ds, dt, ps, k, pt]
} for 4 but exactly 2 State, 6 Int

check CopyPostWellFormed for 5 but exactly 2 State, 6 Int
check CopyNewLength for 5 but exactly 2 State, 6 Int
check ShiftPreservesValues for 5 but exactly 2 State, 6 Int
