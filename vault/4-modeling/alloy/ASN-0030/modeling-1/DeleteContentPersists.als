-- ASN-0030 A4(b) — DeleteContentPersists
-- Lemma: for each position j in [p, p+k) of DELETE(d, p, k),
--   let a = Σ.V(d)(j): a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a)
-- Follows from A4(a) (Σ'.I = Σ.I) and P2 (ReferentiallyComplete).

sig Addr {}
sig Identity {}
sig Document {}

sig State {
  docs: set Document,
  imap: Addr -> lone Identity,
  -- V(d)(j) = a: document d at position j holds address a
  vmap: Document -> Int -> lone Addr
} {
  -- V-space only for active documents
  (vmap.Addr).Int in docs
  -- Positions are positive
  all d: docs, j: Int | some d.vmap[j] implies j >= 1
  -- P2 (ReferentiallyComplete): every V-space address is in dom(I)
  Int.(docs.vmap) in imap.Identity
}

fun idom[s: State]: set Addr {
  s.imap.Identity
}

-- DELETE precondition (A4 pre)
pred DeletePre[s: State, d: Document, p, k: Int] {
  d in s.docs
  p >= 1
  k >= 1
  let last = plus[p, minus[k, 1]] {
    last >= p                    -- overflow guard
    -- all deleted positions are defined
    all j: Int | (j >= p and j =< last) implies some d.(s.vmap)[j]
  }
}

-- DELETE operation: precondition + A4(a) frame
pred Delete[s, s2: State, d: Document, p, k: Int] {
  DeletePre[s, d, p, k]
  -- A4(a): I-space unchanged
  s2.imap = s.imap
  -- A4(g): doc set unchanged
  s2.docs = s.docs
  -- A4(f): other docs unchanged
  all d2: s.docs - d | d2.(s2.vmap) = d2.(s.vmap)
}

-- A4(b): addresses at deleted positions persist in I-space
assert DeleteContentPersists {
  all s, s2: State, d: Document, p, k: Int |
    Delete[s, s2, d, p, k] implies {
      let last = plus[p, minus[k, 1]] |
        all j: Int | (j >= p and j =< last) implies
          let a = d.(s.vmap)[j] {
            a in idom[s2]
            s2.imap[a] = s.imap[a]
          }
    }
}

-- Non-vacuity: a valid DELETE exists
run FindDelete {
  some s, s2: State, d: Document, p, k: Int |
    Delete[s, s2, d, p, k]
} for 4 but exactly 2 State, 6 Int

check DeleteContentPersists for 5 but exactly 2 State, 6 Int
