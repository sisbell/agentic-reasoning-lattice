-- ASN-0030 A6 — VersionCorrespondence (LEMMA)
-- At the moment of version creation, for source document d_s and new version d_v:
--   (A p : 1 ≤ p ≤ |Σ.V(d_s)| : correspond(d_s, p, d_v, p))
-- Derived from D12 (VersionCreation, ASN-0029):
--   Σ'.V(d_v)(p) = Σ.V(d_s)(p) for all valid positions, and Σ'.I = Σ.I.

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

-- Correspond: two (doc, pos) pairs resolve to the same I-address in state s.
-- Within one state the interpretation map I is shared, so address equality
-- implies content equality.
pred correspond[s: State, d1: Document, p1: Int, d2: Document, p2: Int] {
  some d1.(s.vmap)[p1]
  d1.(s.vmap)[p1] = d2.(s.vmap)[p2]
}

-- D12: Version creation
-- Creates new document d_v as a version of d_s, copying V-list exactly.
pred VersionCreate[s, s2: State, ds, dv: Document] {
  -- Preconditions
  wellFormed[s, ds]
  dv not in s.docs

  -- V-list copy: new version gets source's V-list
  all p: Int | dv.(s2.vmap)[p] = ds.(s.vmap)[p]

  -- Frame: source doc V-list unchanged
  all p: Int | ds.(s2.vmap)[p] = ds.(s.vmap)[p]

  -- Frame: other docs unchanged
  all d: s.docs - ds | d.(s2.vmap) = d.(s.vmap)

  -- New doc set
  s2.docs = s.docs + dv
}

-- A6: VersionCorrespondence
-- After version creation, source and version correspond at all source positions
assert A6_VersionCorrespondence {
  all s, s2: State, ds, dv: Document |
    VersionCreate[s, s2, ds, dv] implies
      (all p: Int | (p >= 1 and p =< docLen[s, ds]) implies
        correspond[s2, ds, p, dv, p])
}

-- Non-vacuity: version creation is satisfiable with a nonempty source
run FindVersionCreate {
  some s, s2: State, ds, dv: Document |
    VersionCreate[s, s2, ds, dv] and docLen[s, ds] >= 1
} for 4 but exactly 2 State, 6 Int

check A6_VersionCorrespondence for 5 but exactly 2 State, 6 Int
