-- P9 (length) — InsertLength (POST, ensures)
-- After Insert(d, p, k), the document length satisfies |V'(d)| = n_d + k.
--
-- Models V-space structurally: positions [1..n] mapped to Addr atoms.
-- Insert preserves prefix, shifts suffix, fills inserted span.
-- The length postcondition is derived, not assumed.

sig Addr {}
sig DocId {}

sig State {
  docs: set DocId,
  -- V-space: document -> position -> address (total on [1..n_d])
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

-- Well-formedness: vmap defined exactly for docs, positions are dense
pred wfState[s: State] {
  all d: DocId | (some s.vmap[d]) iff d in s.docs
  all d: s.docs | densePositions[s, d]
  -- guard against integer overflow on nd + 1
  all d: s.docs | plus[docLen[s, d], 1] > docLen[s, d]
}

-- Structural Insert: insert k bytes at position pos in document d.
-- Defines what happens to the V-space mapping; does NOT assume the length property.
pred Insert[s, sPost: State, d: DocId, pos: Int, k: Int] {
  d in s.docs
  k >= 1
  pos >= 1
  pos =< plus[docLen[s, d], 1]

  sPost.docs = s.docs

  let nd = docLen[s, d] {
    -- no overflow on nd + k
    plus[nd, k] >= nd

    -- preserved prefix: positions [1..pos-1] keep their addresses
    all i: Int | (i >= 1 and i < pos) implies
      sPost.vmap[d][i] = s.vmap[d][i]

    -- shifted suffix: old position i in [pos..nd] moves to i+k
    all i: Int | (i >= pos and i =< nd) implies
      sPost.vmap[d][plus[i, k]] = s.vmap[d][i]

    -- exactly positions [1..nd+k] are occupied in the post-state
    all i: Int | some sPost.vmap[d][i] iff
      (i >= 1 and i =< plus[nd, k])

    -- frame: other documents unchanged
    all d2: DocId - d | sPost.vmap[d2] = s.vmap[d2]
  }
}

-- P9 (length): Insert yields |V'(d)| = n_d + k
assert InsertLength {
  all s, sPost: State, d: DocId, pos, k: Int |
    (wfState[s] and Insert[s, sPost, d, pos, k]) implies
      docLen[sPost, d] = plus[docLen[s, d], k]
}

-- Non-vacuity: a satisfying Insert instance exists
run NonVacuity {
  some s, sPost: State, d: DocId, pos, k: Int |
    wfState[s] and Insert[s, sPost, d, pos, k]
} for 4 but exactly 2 State, 5 Int

check InsertLength for 4 but exactly 2 State, 5 Int
