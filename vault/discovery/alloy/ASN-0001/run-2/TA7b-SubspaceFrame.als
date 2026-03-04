-- TA7b-SubspaceFrame
-- An INSERT or DELETE within subspace S1 does not modify
-- any position in a distinct subspace S2.
--
-- A subspace is defined by a shared first component (level-1 prefix).
-- Operations within S1 shift level-2 components for content in S1.
-- Content in a distinct subspace S2 (different prefix) is unaffected.

open util/integer

--------------------------------------------------------------
-- Tumbler representation (two-level for subspace checking)
--------------------------------------------------------------

sig Tumbler {
  c1: Int,
  c2: Int
} {
  c1 >= 0
  c2 >= 0
}

fact UniqueTumblers {
  all disj t1, t2: Tumbler |
    t1.c1 != t2.c1 or t1.c2 != t2.c2
}

--------------------------------------------------------------
-- Subspaces
--------------------------------------------------------------

sig Subspace {
  prefix: Int
} {
  prefix >= 0
}

fact UniqueSubspaces {
  all disj s1, s2: Subspace | s1.prefix != s2.prefix
}

pred inSubspace[t: Tumbler, s: Subspace] {
  t.c1 = s.prefix
}

pred distinctSubs[s1, s2: Subspace] {
  s1 != s2
}

--------------------------------------------------------------
-- Content and state
--------------------------------------------------------------

sig Content {}

sig State {
  pos: Content -> one Tumbler
}

--------------------------------------------------------------
-- Tumbler ordering (lexicographic)
--------------------------------------------------------------

pred lte[a, b: Tumbler] {
  a.c1 < b.c1 or (a.c1 = b.c1 and a.c2 =< b.c2)
}

--------------------------------------------------------------
-- Operations within a subspace
--------------------------------------------------------------

-- INSERT: content in s at/after target shifted forward at level 2.
-- All other content unchanged.
pred Insert[pre, post: State, s: Subspace, target: Tumbler] {
  inSubspace[target, s]
  all c: Content | {
    (inSubspace[pre.pos[c], s] and lte[target, pre.pos[c]]) implies {
      post.pos[c].c1 = pre.pos[c].c1
      post.pos[c].c2 = plus[pre.pos[c].c2, 1]
    } else {
      post.pos[c] = pre.pos[c]
    }
  }
}

-- DELETE: content in s strictly after target shifted backward at level 2.
-- All other content unchanged.
pred Delete[pre, post: State, s: Subspace, target: Tumbler] {
  inSubspace[target, s]
  all c: Content | {
    (inSubspace[pre.pos[c], s] and pre.pos[c] != target and
     lte[target, pre.pos[c]]) implies {
      post.pos[c].c1 = pre.pos[c].c1
      post.pos[c].c2 = minus[pre.pos[c].c2, 1]
    } else {
      post.pos[c] = pre.pos[c]
    }
  }
}

pred Operate[pre, post: State, s: Subspace, target: Tumbler] {
  Insert[pre, post, s, target] or Delete[pre, post, s, target]
}

--------------------------------------------------------------
-- Assertion
--------------------------------------------------------------

-- Frame: operation in s1 preserves all positions in distinct s2
assert SubspaceFrame {
  all pre, post: State, s1, s2: Subspace, target: Tumbler |
    (Operate[pre, post, s1, target] and distinctSubs[s1, s2]) implies
    (all c: Content |
      inSubspace[pre.pos[c], s2] implies post.pos[c] = pre.pos[c])
}

--------------------------------------------------------------
-- Non-vacuity
--------------------------------------------------------------

-- Find an insert that actually shifts content while content in s2 exists
run NonVacuity {
  some pre, post: State, s1, s2: Subspace, target: Tumbler |
    Insert[pre, post, s1, target] and
    distinctSubs[s1, s2] and
    pre.pos != post.pos and
    (some c: Content | inSubspace[pre.pos[c], s2])
} for 5 but exactly 2 State, 2 Subspace, 5 Int

--------------------------------------------------------------
-- Check
--------------------------------------------------------------

check SubspaceFrame for 5 but exactly 2 State, 2 Subspace, 5 Int
