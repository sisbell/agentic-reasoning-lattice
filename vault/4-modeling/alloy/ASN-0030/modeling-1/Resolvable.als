-- ASN-0030 Resolvable (INV, predicate)
-- resolvable(L, d) ≡ (E a ∈ endset(L) : reachable(a, d))
-- A link L is resolvable from document d iff at least one address
-- in the endset of L is referenced by d.

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

-- Resolvable is equivalent to a nonempty intersection of endset and refs
assert ResolvableIffOverlap {
  all s: State, L: Link, d: s.docs |
    resolvable[s, L, d] iff some (L.endset & s.refs[d])
}

-- Disjoint endset and refs implies not resolvable
assert DisjointImpliesNotResolvable {
  all s: State, L: Link, d: s.docs |
    no (L.endset & s.refs[d]) implies not resolvable[s, L, d]
}

-- Empty endset implies not resolvable from any document
assert EmptyEndsetNotResolvable {
  all s: State, L: Link, d: s.docs |
    no L.endset implies not resolvable[s, L, d]
}

-- Non-vacuity: find a state where a link is resolvable
run FindResolvable {
  some s: State, L: Link, d: Doc |
    d in s.docs and some L.endset and resolvable[s, L, d]
} for 4 but exactly 1 State

check ResolvableIffOverlap for 5 but exactly 1 State
check DisjointImpliesNotResolvable for 5 but exactly 1 State
check EmptyEndsetNotResolvable for 5 but exactly 1 State
