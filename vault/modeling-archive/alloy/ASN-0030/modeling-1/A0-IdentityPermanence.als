-- A0-IdentityPermanence.als
-- Property: for any state transition Σ → Σ',
--   a ∈ dom(Σ.I) ⟹ a ∈ dom(Σ'.I) ∧ Σ'.I(a) = Σ.I(a)
-- Conjunction of ISpaceImmutable (P0) and ISpaceMonotone (P1).

sig Addr {}

sig Identity {}

sig State {
  imap: Addr -> lone Identity
}

-- The domain of I is the set of addresses with an identity assigned.
fun idom[s: State]: set Addr {
  s.imap.Identity
}

-- A valid state transition: constrained by IdentityPermanence.
-- We model a general transition predicate that the property constrains.
pred transition[s, s2: State] {
  -- IdentityPermanence: every address in dom(s.I) stays with same identity
  all a: idom[s] | s2.imap[a] = s.imap[a]
}

-- Assert: IdentityPermanence holds for all transitions satisfying
-- the transition predicate. This is definitional — the check confirms
-- the encoding is consistent and non-vacuous together with the run.

-- P1 (ISpaceMonotone): dom(I) only grows
assert MonotoneFromPermanence {
  all s, s2: State |
    transition[s, s2] implies idom[s] in idom[s2]
}

-- P0 (ISpaceImmutable): identity values are preserved
assert ImmutableFromPermanence {
  all s, s2: State, a: Addr |
    (transition[s, s2] and a in idom[s]) implies s2.imap[a] = s.imap[a]
}

-- Combined: the conjunction
assert IdentityPermanence {
  all s, s2: State |
    transition[s, s2] implies
      (idom[s] in idom[s2] and
       all a: idom[s] | s2.imap[a] = s.imap[a])
}

-- Non-vacuity: a transition exists where pre-state has a nonempty imap
-- and post-state extends it with a new address.
run NonVacuous {
  some s, s2: State, a, a2: Addr |
    a != a2 and
    a in idom[s] and
    a2 not in idom[s] and
    transition[s, s2] and
    a2 in idom[s2]
} for 4 but exactly 2 State

check MonotoneFromPermanence for 5 but exactly 2 State
check ImmutableFromPermanence for 5 but exactly 2 State
check IdentityPermanence for 5 but exactly 2 State
