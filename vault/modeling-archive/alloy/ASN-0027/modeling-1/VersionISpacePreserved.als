-- A5.frame-I — VersionISpacePreserved (FRAME, ensures)
-- Property: Σ'.I = Σ.I
-- The Version operation preserves the I-space.

sig Addr {}
sig Char {}
sig Doc {}

sig State {
  ispace: Addr -> lone Char,
  docs: set Doc,
  ver: Doc -> Int -> lone Addr
}

pred wellFormed[s: State] {
  all d: Doc - s.docs | no s.ver[d]
  all d: s.docs {
    all i: Int | some s.ver[d][i] implies i >= 1
    all i, j: Int |
      (j >= 1 and j =< i and some s.ver[d][i]) implies some s.ver[d][j]
  }
}

-- A5: Version operation — create new document sharing source's version list
pred Version[s, sPost: State, d, dNew: Doc] {
  -- preconditions
  d in s.docs
  dNew not in s.docs

  -- postcondition: new doc added
  sPost.docs = s.docs + dNew

  -- postcondition: version list of dNew identical to d
  sPost.ver[dNew] = s.ver[d]

  -- frame: existing doc versions unchanged
  all d2: s.docs | sPost.ver[d2] = s.ver[d2]

  -- frame: I-space preserved
  sPost.ispace = s.ispace
}

-- A5.frame-I: Version preserves I-space
assert VersionISpacePreserved {
  all s, sPost: State, d, dNew: Doc |
    Version[s, sPost, d, dNew] implies sPost.ispace = s.ispace
}

-- Non-vacuity: find a valid Version with non-empty I-space
run NonVacuity {
  some s, sPost: State, d, dNew: Doc |
    wellFormed[s] and Version[s, sPost, d, dNew] and some s.ispace
} for 5 but exactly 2 State, 4 Int

check VersionISpacePreserved for 5 but exactly 2 State, 4 Int
