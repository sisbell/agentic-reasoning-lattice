-- ASN-0026 P0 — ISpaceImmutable
-- [a in dom(Sigma.I) ==> Sigma'.I(a) = Sigma.I(a)]
-- I-space content is immutable across any state transition.

sig Addr {}
sig Byte {}

sig State {
  ispace: Addr -> lone Byte   -- Sigma.I : Addr ⇀ Byte
}

-- Domain of I-space: addresses that have a mapping
fun dom[s: State]: set Addr {
  s.ispace.Byte
}

-- A legal transition must preserve all existing I-space bindings.
-- New addresses may be allocated, but existing ones never change.
pred transition[s, sPost: State] {
  -- I-space immutability constraint
  all a: dom[s] | sPost.ispace[a] = s.ispace[a]
}

-- P0: ISpaceImmutable holds for any transition
assert ISpaceImmutable {
  all s, sPost: State |
    transition[s, sPost] implies
      (all a: Addr | a in dom[s] implies sPost.ispace[a] = s.ispace[a])
}

check ISpaceImmutable for 5 but exactly 2 State

-- Non-vacuity: a transition exists where the pre-state has content
-- and the post-state adds a new address
run NonVacuity {
  some s, sPost: State |
    s != sPost and
    some dom[s] and
    transition[s, sPost] and
    some dom[sPost] - dom[s]
} for 5 but exactly 2 State
