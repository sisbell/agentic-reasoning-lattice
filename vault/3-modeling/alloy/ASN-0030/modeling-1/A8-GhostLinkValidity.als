-- ASN-0030 A8 — GhostLinkValidity (INV, predicate(Link, State))
-- ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)
-- A link L has ghost addresses when (E a ∈ endset(L) : ghost(a)).
-- Such addresses are well-formed tumblers with no content until
-- transition (iii)→(i).

sig Addr {}

-- T4 addresses: well-formed tumblers (subset signature)
sig T4Addr in Addr {}

-- A link has an endset: the set of I-addresses covered by its spans
-- (from, to, type spans unioned). Abstracted as a plain set.
sig Link {
  endset: set Addr
}

sig State {
  content: set Addr,   -- dom(Σ.I): addresses with allocated content
  links: set Link
}

-- ghost(a) ≡ a ∉ dom(Σ.I) ∧ T4(a)
pred ghost[a: Addr, s: State] {
  a not in s.content
  a in T4Addr
}

-- GhostLinkValidity: (E a ∈ endset(L) : ghost(a))
pred ghostLinkValid[l: Link, s: State] {
  some a: l.endset | ghost[a, s]
}

-- Well-formed state: every endset address outside dom(I) must be T4.
-- This is the structural validity constraint — non-T4 addresses outside
-- content would be ill-formed references, not ghosts.
pred wellFormed[s: State] {
  all l: s.links, a: l.endset |
    a not in s.content implies a in T4Addr
}

-- A8: In a well-formed state, any link with endset addresses beyond
-- the content map has ghost addresses (the non-content addresses are
-- T4 by wellFormed, hence ghost by definition).
assert A8_GhostLinkValidity {
  all s: State, l: s.links |
    (wellFormed[s] and some (l.endset - s.content))
      implies ghostLinkValid[l, s]
}

-- Contrapositive: if every endset address has content, no ghosts exist
assert NoGhostWhenFullyMapped {
  all s: State, l: s.links |
    l.endset in s.content implies not ghostLinkValid[l, s]
}

-- Ghost implies T4 (definitional sanity)
assert GhostImpliesT4 {
  all s: State, a: Addr |
    ghost[a, s] implies a in T4Addr
}

-- Non-vacuity: a well-formed state with a ghost-valid link exists
run FindGhostLink {
  some s: State, l: s.links |
    wellFormed[s] and ghostLinkValid[l, s] and some (l.endset & s.content)
} for 4 but exactly 1 State

check A8_GhostLinkValidity for 5
check NoGhostWhenFullyMapped for 5
check GhostImpliesT4 for 5
