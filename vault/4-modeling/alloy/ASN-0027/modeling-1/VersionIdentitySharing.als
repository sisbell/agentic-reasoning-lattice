-- A5.identity — VersionIdentitySharing (POST, ensures)
-- After A5.new, the new document d' has the same version list as source d:
--   |V(d')| = n_d  and  forall j in 1..n_d: V(d')(j) = V(d)(j)

sig Addr {}
sig Doc {}

sig State {
  docs: set Doc,
  ver: Doc -> Int -> lone Addr
}

-- Number of versions for document d in state s
fun nd[s: State, d: Doc]: Int {
  #(s.ver[d])
}

-- Version lists are 1-indexed and contiguous
pred wellFormed[s: State] {
  -- only known docs have versions
  all d: Doc - s.docs | no s.ver[d]
  -- versions are 1-indexed and contiguous
  all d: s.docs {
    all i: Int | some s.ver[d][i] implies i >= 1
    all i, j: Int |
      (j >= 1 and j =< i and some s.ver[d][i]) implies some s.ver[d][j]
  }
}

-- A5.new: create new document sharing source's version list
pred A5_new[s, sPost: State, d, dNew: Doc] {
  -- preconditions
  d in s.docs
  dNew not in s.docs
  some s.ver[d]

  -- postcondition: new doc added
  sPost.docs = s.docs + dNew

  -- postcondition: version list of dNew is identical to d
  sPost.ver[dNew] = s.ver[d]

  -- frame: existing doc versions unchanged
  all d2: s.docs | sPost.ver[d2] = s.ver[d2]
}

-- A5.identity: version identity sharing
assert VersionIdentitySharing {
  all s, sPost: State, d, dNew: Doc |
    (wellFormed[s] and A5_new[s, sPost, d, dNew]) implies {
      -- same length
      nd[sPost, dNew] = nd[s, d]
      -- same content at each position
      all j: Int | (j >= 1 and j =< nd[s, d]) implies
        sPost.ver[dNew][j] = s.ver[d][j]
    }
}

-- A5_new preserves well-formedness
assert A5_newPreservesWF {
  all s, sPost: State, d, dNew: Doc |
    (wellFormed[s] and A5_new[s, sPost, d, dNew]) implies wellFormed[sPost]
}

check VersionIdentitySharing for 5 but exactly 2 State, 4 Int
check A5_newPreservesWF for 5 but exactly 2 State, 4 Int

-- Non-vacuity: the operation can fire
run NonVacuity {
  some s, sPost: State, d, dNew: Doc |
    wellFormed[s] and A5_new[s, sPost, d, dNew] and wellFormed[sPost]
} for 5 but exactly 2 State, 4 Int
