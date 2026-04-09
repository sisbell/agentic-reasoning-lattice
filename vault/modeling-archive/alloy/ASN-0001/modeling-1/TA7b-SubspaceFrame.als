-- TA7b: SubspaceFrame
-- An INSERT or DELETE within subspace S1 does not modify any position in a
-- distinct subspace S2: (A b in S2 : post(b) = pre(b)).
--
-- Key structural fact: each V-space position belongs to exactly one subspace
-- (determined by the tumbler's node/user/document field prefix, modeled abstractly).
-- Distinct subspaces therefore contain disjoint positions.  An operation that
-- only touches positions in S1 cannot touch any position in S2 ≠ S1.

sig Subspace {}

sig Content {}

-- Each position in V-space belongs to exactly one subspace.
-- (In concrete terms this is the node.user.document prefix of the tumbler.)
sig Position {
  owner: one Subspace
}

-- V-space state: the current address of each live content item.
sig State {
  pos: Content -> lone Position
}

-- Addresses are injective: no two content items share a position.
fact PositionsInjective {
  all s: State, p: Position | lone s.pos.p
}

-- An operation is "within subspace s" when every position change involves s:
--   • any position newly assigned to a content item belongs to s
--   • any position released (removed or replaced) by a content item belonged to s
-- This covers INSERT (new position in s, no old), DELETE (no new position, old in s),
-- and MOVE within s (both old and new in s).
pred OperationWithin[pre, post: State, s: Subspace] {
  all c: Content {
    -- newly assigned or changed target is in s
    (some post.pos[c] and post.pos[c] != pre.pos[c]) implies
      post.pos[c].owner = s
    -- released or changed source was in s
    (some pre.pos[c] and (no post.pos[c] or post.pos[c] != pre.pos[c])) implies
      pre.pos[c].owner = s
  }
}

-- SubspaceFrame: an operation within S1 leaves every S2-position unchanged (S1 ≠ S2).
-- Proof sketch: if pre.pos[b].owner = s2 and s1 ≠ s2, then OperationWithin's
-- second clause forces pre.pos[b].owner = s1 — contradiction — so b's position
-- cannot change.
assert SubspaceFrame {
  all pre, post: State, s1, s2: Subspace |
    (s1 != s2 and OperationWithin[pre, post, s1]) implies
      all b: Content |
        pre.pos[b].owner = s2 implies post.pos[b] = pre.pos[b]
}

-- Non-vacuity: confirm the model admits an operation in s1 with content
-- present in both subspaces (so the frame constraint is non-trivially exercised).
run NonVacuous {
  some pre, post: State, s1, s2: Subspace |
    s1 != s2 and
    OperationWithin[pre, post, s1] and
    (some b: Content | pre.pos[b].owner = s2) and
    (some c: Content | some pre.pos[c] and pre.pos[c].owner = s1)
} for 5 but exactly 2 State, exactly 2 Subspace

check SubspaceFrame for 5 but exactly 2 State
