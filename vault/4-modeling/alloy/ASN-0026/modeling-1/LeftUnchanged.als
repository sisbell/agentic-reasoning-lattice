-- P9 (left) — LeftUnchanged (FRAME, ensures)
-- After Insert(d, p, k), positions before the insertion point are unchanged:
--   (A j : 1 <= j < p : Sigma'.V(d)(j) = Sigma.V(d)(j))
--
-- Models V-space structurally: positions [1..n] mapped to Addr atoms.
-- Insert defines suffix shift, new-span allocation, and position bounds.
-- LeftUnchanged is asserted as a derived frame property.

sig Addr {}
sig DocId {}

sig State {
  docs: set DocId,
  vmap: DocId -> Int -> lone Addr
}

-- Positions occupied by document d in state s
fun positions[s: State, d: DocId]: set Int {
  (s.vmap[d]).Addr
}

-- Length of document d in state s
fun docLen[s: State, d: DocId]: Int {
  #positions[s, d]
}

-- Positions form a dense interval [1..n] with no gaps
pred densePositions[s: State, d: DocId] {
  let ps = positions[s, d], n = #ps {
    all p: ps | p >= 1 and p =< n
    all i: Int | (i >= 1 and i =< n) implies i in ps
  }
}

-- Well-formedness: vmap defined exactly for docs, positions dense
pred wfState[s: State] {
  all d: DocId | (some s.vmap[d]) iff d in s.docs
  all d: s.docs | densePositions[s, d]
  all d: s.docs | plus[docLen[s, d], 1] > docLen[s, d]
}

-- Structural Insert: insert k bytes at position pos in document d.
-- Specifies suffix shift, new-span coverage, and exact position bounds.
-- The prefix clause (positions < pos unchanged) is NOT included here;
-- LeftUnchanged is asserted separately as a derivable frame property.
pred Insert[s, sPost: State, d: DocId, pos: Int, k: Int] {
  d in s.docs
  k >= 1
  pos >= 1
  pos =< plus[docLen[s, d], 1]

  sPost.docs = s.docs

  let nd = docLen[s, d] {
    plus[nd, k] >= nd

    -- shifted suffix: old position i in [pos..nd] moves to i+k
    all i: Int | (i >= pos and i =< nd) implies
      sPost.vmap[d][plus[i, k]] = s.vmap[d][i]

    -- new span [pos..pos+k-1] each maps to some address
    all i: Int | (i >= pos and i < plus[pos, k]) implies
      some sPost.vmap[d][i]

    -- exactly positions [1..nd+k] are occupied in the post-state
    all i: Int | some sPost.vmap[d][i] iff
      (i >= 1 and i =< plus[nd, k])

    -- frame: other documents unchanged
    all d2: DocId - d | sPost.vmap[d2] = s.vmap[d2]
  }
}

-- P9 (left): positions before the insertion point are unchanged
assert LeftUnchanged {
  all s, sPost: State, d: DocId, pos, k: Int |
    (wfState[s] and Insert[s, sPost, d, pos, k]) implies
      (all j: Int | (j >= 1 and j < pos) implies
        sPost.vmap[d][j] = s.vmap[d][j])
}

-- Non-vacuity: a satisfying Insert instance exists
run NonVacuity {
  some s, sPost: State, d: DocId, pos, k: Int |
    wfState[s] and Insert[s, sPost, d, pos, k]
} for 4 but exactly 2 State, 5 Int

check LeftUnchanged for 4 but exactly 2 State, 5 Int
