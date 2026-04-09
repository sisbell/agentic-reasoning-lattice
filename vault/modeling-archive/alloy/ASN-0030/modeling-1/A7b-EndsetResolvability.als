-- ASN-0030 A7b — EndsetResolvability (LEMMA)
-- ¬[resolvable(L, d) in Σ ⟹ resolvable(L, d) in Σ']
-- Witness: DELETE on d can remove V-space mappings that made L's
-- endpoints reachable through d.
-- Resolvability of a link through a document is NOT preserved by
-- arbitrary operations; DELETE can break it.

sig Addr {}

sig Doc {}

-- A link has an endset: the set of I-addresses covered by its spans
-- (from, to, type spans unioned). Abstracted as a plain set.
sig Link {
  endset: set Addr
}

sig State {
  docs: set Doc,
  refs: Doc -> set Addr    -- refs(d): addresses referenced by document d
}

-- reachable(a, d): address a is referenced by document d
pred reachable[s: State, a: Addr, d: Doc] {
  d in s.docs
  a in s.refs[d]
}

-- resolvable(L, d): some address in endset(L) is reachable from d
pred resolvable[s: State, L: Link, d: Doc] {
  some a: L.endset | reachable[s, a, d]
}

-- Delete operation: remove some refs from document d's V-space
pred Delete[s, s2: State, d: Doc] {
  -- precondition: d is a document in both states
  d in s.docs
  d in s2.docs
  -- some references are removed from d
  s2.refs[d] in s.refs[d]
  some s.refs[d] - s2.refs[d]
  -- frame: other documents' refs unchanged, doc set unchanged
  all d2: Doc - d | s2.refs[d2] = s.refs[d2]
  s2.docs = s.docs
}

-- A7b: assert the implication (expect counterexample)
-- If this were true, resolvability would be preserved by Delete.
-- A counterexample demonstrates that Delete can break resolvability.
assert EndsetResolvability {
  all s, s2: State, L: Link, d: Doc |
    (resolvable[s, L, d] and Delete[s, s2, d])
      implies resolvable[s2, L, d]
}

-- Non-vacuity: Delete can happen when a link is resolvable
run NonVacuity {
  some s, s2: State, L: Link, d: Doc |
    resolvable[s, L, d] and Delete[s, s2, d]
} for 4 but exactly 2 State

check EndsetResolvability for 5 but exactly 2 State
