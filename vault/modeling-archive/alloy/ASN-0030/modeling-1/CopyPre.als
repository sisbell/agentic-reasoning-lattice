-- ASN-0030 A5 pre — CopyPre
-- Precondition for COPY(d_s, p_s, k, d_t, p_t):
--   d_s ∈ Σ.D ∧ d_t ∈ Σ.D ∧ k ≥ 1
--   ∧ 1 ≤ p_s ∧ p_s + k − 1 ≤ n_{d_s}
--   ∧ 1 ≤ p_t ≤ n_{d_t} + 1

sig Document {}

sig State {
  docs: set Document,
  len: Document -> lone Int
} {
  -- len is defined exactly on docs
  len.Int = docs
  -- bound lengths to avoid integer overflow at 6-bit width
  all d: docs | d.len >= 0 and d.len =< 15
}

-- COPY precondition (with overflow guard)
pred CopyPre[s: State, ds, dt: Document, ps, k, pt: Int] {
  ds in s.docs
  dt in s.docs
  k >= 1
  ps >= 1
  let srcEnd = plus[ps, minus[k, 1]] {
    -- overflow guard: srcEnd must not wrap below ps
    srcEnd >= ps
    srcEnd =< ds.(s.len)
  }
  pt >= 1
  pt =< plus[dt.(s.len), 1]
}

-- Source range is within document bounds
assert SourceInBounds {
  all s: State, ds, dt: Document, ps, k, pt: Int |
    CopyPre[s, ds, dt, ps, k, pt] implies ps =< ds.(s.len)
}

-- Copy count does not exceed source document length
assert CopyBounded {
  all s: State, ds, dt: Document, ps, k, pt: Int |
    CopyPre[s, ds, dt, ps, k, pt] implies k =< ds.(s.len)
}

-- Source document has at least one position
assert SourceNonEmpty {
  all s: State, ds, dt: Document, ps, k, pt: Int |
    CopyPre[s, ds, dt, ps, k, pt] implies ds.(s.len) >= 1
}

-- Target position is at most one past end (insertion point)
assert TargetInBounds {
  all s: State, ds, dt: Document, ps, k, pt: Int |
    CopyPre[s, ds, dt, ps, k, pt] implies
      (pt >= 1 and pt =< plus[dt.(s.len), 1])
}

-- Self-copy is permitted (d_s = d_t not excluded)
run FindSelfCopy {
  some s: State, d: Document, ps, k, pt: Int |
    CopyPre[s, d, d, ps, k, pt]
} for 4 but exactly 1 State, 6 Int

-- Copy into an empty target document is permitted (p_t = 1, n_{d_t} = 0)
run FindCopyIntoEmpty {
  some s: State, ds, dt: Document, ps, k, pt: Int |
    CopyPre[s, ds, dt, ps, k, pt] and dt.(s.len) = 0
} for 4 but exactly 1 State, 6 Int

-- Non-vacuity: a valid COPY precondition exists
run FindCopy {
  some s: State, ds, dt: Document, ps, k, pt: Int |
    CopyPre[s, ds, dt, ps, k, pt]
} for 4 but exactly 1 State, 6 Int

check SourceInBounds for 5 but exactly 1 State, 6 Int
check CopyBounded for 5 but exactly 1 State, 6 Int
check SourceNonEmpty for 5 but exactly 1 State, 6 Int
check TargetInBounds for 5 but exactly 1 State, 6 Int
