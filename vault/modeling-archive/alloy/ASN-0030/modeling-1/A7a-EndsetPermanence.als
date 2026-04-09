-- ASN-0030 A7a — EndsetPermanence (LEMMA)
-- For any link L, endset addresses in dom(Σ.I) remain in dom(Σ'.I):
--   (A a ∈ endset(L) : a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I))
-- Restriction of P1 (ISpaceMonotone, ASN-0026) to endset members.
-- Follows from A0 (IdentityPermanence): identity preservation implies
-- domain monotonicity.

sig Addr {}

sig Identity {}

-- A link has an endset: the set of I-addresses covered by its
-- from, to, and type spans. Abstracted here as a plain set.
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

-- A0 (IdentityPermanence): every address in dom(I) keeps its identity.
-- This implies P1 (ISpaceMonotone): dom(I) only grows.
pred A0_transition[s, s2: State] {
  all a: idom[s] | s2.imap[a] = s.imap[a]
}

-- P1 derived from A0: domain monotonicity
assert P1_MonotoneFromA0 {
  all s, s2: State |
    A0_transition[s, s2] implies idom[s] in idom[s2]
}

-- A7a: EndsetPermanence
-- Under A0, every endset address in dom(Σ.I) remains in dom(Σ'.I).
assert A7a_EndsetPermanence {
  all s, s2: State, L: Link |
    A0_transition[s, s2] implies
      (all a: L.endset | a in idom[s] implies a in idom[s2])
}

-- Non-vacuity: a link with a nonempty endset partly in dom(I),
-- and a transition that extends I with a new address.
run NonVacuous {
  some s, s2: State, L: Link, a, a2: Addr |
    a != a2 and
    a in L.endset and
    a in idom[s] and
    A0_transition[s, s2] and
    a2 not in idom[s] and
    a2 in idom[s2]
} for 4 but exactly 2 State

check P1_MonotoneFromA0 for 5 but exactly 2 State
check A7a_EndsetPermanence for 5 but exactly 2 State
