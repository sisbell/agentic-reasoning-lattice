-- ASN-0030 A7 — LinkTargetStability (LEMMA)
-- For any link L whose endset addresses are in dom(Σ.I), any operation
-- preserves I-space content at those addresses:
--   (A a ∈ endset(L) : Σ'.I(a) = Σ.I(a))
-- Derived from A0 (IdentityPermanence): once an address is in dom(I),
-- its identity never changes.

sig Addr {}

sig Identity {}

-- A link has an endset: the set of I-addresses covered by its spans
-- (from, to, type spans unioned). Abstracted here as a plain set.
sig Link {
  endset: set Addr
}

sig State {
  imap: Addr -> lone Identity
}

-- Domain of the identity map
fun idom[s: State]: set Addr {
  s.imap.Identity
}

-- A0 (IdentityPermanence): every address in dom(I) keeps its identity
pred A0_transition[s, s2: State] {
  all a: idom[s] | s2.imap[a] = s.imap[a]
}

-- Precondition: all endset addresses are in dom(I)
pred endsetInDomain[L: Link, s: State] {
  L.endset in idom[s]
}

-- A7: LinkTargetStability
-- Under A0, if endset(L) ⊆ dom(I), then identity at every endset
-- address is preserved across any transition.
assert A7_LinkTargetStability {
  all s, s2: State, L: Link |
    (endsetInDomain[L, s] and A0_transition[s, s2]) implies
      (all a: L.endset | s2.imap[a] = s.imap[a])
}

-- Non-vacuity: a link with nonempty endset in dom(I),
-- and a transition that extends I with a new address.
run NonVacuous {
  some s, s2: State, L: Link, a, a2: Addr |
    a != a2 and
    a in L.endset and
    endsetInDomain[L, s] and
    A0_transition[s, s2] and
    a2 not in idom[s] and
    a2 in idom[s2]
} for 4 but exactly 2 State

check A7_LinkTargetStability for 5 but exactly 2 State
