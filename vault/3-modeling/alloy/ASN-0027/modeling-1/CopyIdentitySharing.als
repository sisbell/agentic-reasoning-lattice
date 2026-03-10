-- A4.identity — CopyIdentitySharing (POST, ensures)
-- Property: (A j : 0 =< j < k : Sigma'.V(d_t)(p_t + j) = Sigma.V(d_s)(p_s + j))
-- After Copy, each target slot holds the same address as the corresponding
-- source slot in the pre-state.  "Identity sharing" — same Addr atom, not a copy.

open util/integer

sig Addr {}
sig Doc {}

sig State {
  V: Doc -> Int -> lone Addr,
  len: Doc -> one Int
}

pred wellFormed[s: State] {
  all d: Doc {
    s.len[d] >= 1
    s.len[d] =< 10
    all j: Int | (j >= 1 and j =< s.len[d]) implies one s.V[d][j]
    all j: Int | (j < 1 or j > s.len[d]) implies no s.V[d][j]
  }
}

-- Overflow guard
pred bounded[ps: Int, k: Int, pt: Int] {
  ps >= 0 and ps =< 10
  k  >= 0 and k  =< 10
  pt >= 0 and pt =< 10
}

-- Copy precondition (from A4.pre)
pred CopyPre[s: State, ds: Doc, dt: Doc, ps: Int, k: Int, pt: Int] {
  k >= 1
  ps >= 1
  plus[ps, minus[k, 1]] =< s.len[ds]
  pt >= 1
  pt =< plus[s.len[dt], 1]
}

-- A4.identity as standalone predicate
pred A4_identity[s, sPost: State, ds: Doc, dt: Doc, ps: Int, k: Int, pt: Int] {
  all j: Int | (j >= 0 and j < k) implies
    sPost.V[dt][plus[pt, j]] = s.V[ds][plus[ps, j]]
}

-- Copy operation with A4.identity as postcondition
pred Copy[s, sPost: State, ds: Doc, dt: Doc, ps: Int, k: Int, pt: Int] {
  CopyPre[s, ds, dt, ps, k, pt]

  -- POST: A4.identity — target slots get source addresses
  A4_identity[s, sPost, ds, dt, ps, k, pt]

  -- target document length: max(old length, pt + k - 1)
  let copyEnd = plus[pt, minus[k, 1]] |
    sPost.len[dt] = ((copyEnd > s.len[dt]) implies copyEnd else s.len[dt])

  -- frame: positions in dt outside [pt, pt+k) are unchanged
  all j: Int | (j >= 1 and j =< sPost.len[dt] and (j < pt or j >= plus[pt, k])) implies
    sPost.V[dt][j] = s.V[dt][j]

  -- no values outside valid range in dt
  all j: Int | (j < 1 or j > sPost.len[dt]) implies no sPost.V[dt][j]

  -- cross-document frame
  all d: Doc - dt {
    sPost.len[d] = s.len[d]
    sPost.V[d] = s.V[d]
  }
}

-- Sanity: Copy entails A4.identity
assert CopyEntailsIdentity {
  all s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
    (wellFormed[s] and bounded[ps, k, pt] and Copy[s, sPost, ds, dt, ps, k, pt])
    implies A4_identity[s, sPost, ds, dt, ps, k, pt]
}

-- After copy, every target position in [pt, pt+k) is populated
assert CopyTargetPopulated {
  all s, sPost: State, ds, dt: Doc, ps, k, pt: Int, j: Int |
    (wellFormed[s] and bounded[ps, k, pt]
      and Copy[s, sPost, ds, dt, ps, k, pt]
      and j >= 0 and j < k)
    implies some sPost.V[dt][plus[pt, j]]
}

-- When ds != dt, source positions are preserved in post-state (frame consequence)
assert SourcePreservedCrossDoc {
  all s, sPost: State, ds, dt: Doc, ps, k, pt: Int, j: Int |
    (wellFormed[s] and bounded[ps, k, pt]
      and Copy[s, sPost, ds, dt, ps, k, pt]
      and ds != dt and j >= 0 and j < k)
    implies sPost.V[ds][plus[ps, j]] = s.V[ds][plus[ps, j]]
}

-- Identity sharing in post-state: when ds != dt, target and source
-- point to the same Addr in the post-state (non-trivial consequence
-- combining A4.identity with the cross-document frame)
assert PostStateSharing {
  all s, sPost: State, ds, dt: Doc, ps, k, pt: Int, j: Int |
    (wellFormed[s] and bounded[ps, k, pt]
      and Copy[s, sPost, ds, dt, ps, k, pt]
      and ds != dt and j >= 0 and j < k)
    implies sPost.V[dt][plus[pt, j]] = sPost.V[ds][plus[ps, j]]
}

-- Non-vacuity: find a valid Copy with well-formed pre-state
run FindCopy {
  some s, sPost: State, ds, dt: Doc, ps, k, pt: Int |
    wellFormed[s] and bounded[ps, k, pt] and Copy[s, sPost, ds, dt, ps, k, pt]
    and ds != dt and k > 1
} for 5 but exactly 2 State, 6 Int

check CopyEntailsIdentity for 5 but exactly 2 State, 6 Int
check CopyTargetPopulated for 5 but exactly 2 State, 6 Int
check SourcePreservedCrossDoc for 5 but exactly 2 State, 6 Int
check PostStateSharing for 5 but exactly 2 State, 6 Int
