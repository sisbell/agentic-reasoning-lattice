-- ASN-0030 A5(f) — CopySourceUnchanged
-- Frame condition: when source and target are distinct documents,
-- the source V-list is unchanged after COPY.
--   d_s ≠ d_t ⟹ Σ'.V(d_s) = Σ.V(d_s)

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

-- COPY precondition (ASN-0030 A5 pre)
pred CopyPre[s: State, ds, dt: Document, ps, k, pt: Int] {
  wellFormed[s, ds]
  wellFormed[s, dt]
  k >= 1
  ps >= 1
  let srcEnd = plus[ps, minus[k, 1]] {
    srcEnd >= ps             -- overflow guard
    srcEnd =< docLen[s, ds]
  }
  pt >= 1
  pt =< plus[docLen[s, dt], 1]
}

-- COPY operation: postconditions A5(a)-(e) + frame
pred Copy[s, s2: State, ds, dt: Document, ps, k, pt: Int] {
  CopyPre[s, ds, dt, ps, k, pt]
  let nt = docLen[s, dt] {
    -- A5(a): target positions share source I-addresses
    all j: Int | (j >= 0 and j < k) implies
      dt.(s2.vmap)[plus[pt, j]] = ds.(s.vmap)[plus[ps, j]]
    -- A5(d): left frame — positions before p_t unchanged
    all j: Int | (j >= 1 and j < pt) implies
      dt.(s2.vmap)[j] = dt.(s.vmap)[j]
    -- A5(e): right shift — positions at and above p_t shift by k
    all j: Int | (j >= pt and j =< nt) implies
      dt.(s2.vmap)[plus[j, k]] = dt.(s.vmap)[j]
    -- nothing beyond new length
    all j: Int | (j < 1 or j > plus[nt, k]) implies
      no dt.(s2.vmap)[j]
  }
  -- frame: other documents unchanged
  all d2: s.docs - dt | d2.(s2.vmap) = d2.(s.vmap)
  s2.docs = s.docs
}

-- A5(f): source document unchanged when d_s ≠ d_t
assert CopySourceUnchanged {
  all s, s2: State, ds, dt: Document, ps, k, pt: Int |
    (Copy[s, s2, ds, dt, ps, k, pt] and ds != dt) implies
      ds.(s2.vmap) = ds.(s.vmap)
}

-- Non-vacuity: a valid cross-document copy exists
run FindCrossCopy {
  some s, s2: State, ds, dt: Document, ps, k, pt: Int |
    Copy[s, s2, ds, dt, ps, k, pt] and ds != dt
} for 4 but exactly 2 State, 6 Int

check CopySourceUnchanged for 5 but exactly 2 State, 6 Int
