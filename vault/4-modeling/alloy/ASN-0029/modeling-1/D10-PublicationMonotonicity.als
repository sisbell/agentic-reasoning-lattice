-- D10 — PublicationMonotonicity (INV, predicate(State, State))
--
--   Σ.pub(d) = published ⟹ Σ'.pub(d) = published
--
-- Once a document is published, it remains published across every
-- state transition.  Unconditional over all protocol operations.

sig Doc {}

abstract sig PubStatus {}
one sig Private, Published, Privashed extends PubStatus {}

sig State {
  D: set Doc,
  pub: Doc -> lone PubStatus
} {
  pub in D -> PubStatus
  all d: D | one pub[d]
}

----------------------------------------------------------------------
-- Operations
----------------------------------------------------------------------

-- Create a fresh document (enters as private per D0)
pred CreateDoc[s, s2: State, d: Doc] {
  d not in s.D
  s2.D = s.D + d
  s2.pub[d] = Private
  all d2: s.D | s2.pub[d2] = s.pub[d2]
}

-- Change publication status (only from private, per D10a)
pred SetPub[s, s2: State, d: Doc, target: PubStatus] {
  d in s.D
  s.pub[d] = Private
  target in Published + Privashed
  s2.D = s.D
  s2.pub[d] = target
  all d2: s.D - d | s2.pub[d2] = s.pub[d2]
}

-- No-op
pred Skip[s, s2: State] {
  s2.D = s.D
  s2.pub = s.pub
}

-- System step: any operation
pred Step[s, s2: State] {
  (some d: Doc | CreateDoc[s, s2, d])
  or (some d: Doc, t: PubStatus | SetPub[s, s2, d, t])
  or Skip[s, s2]
}

----------------------------------------------------------------------
-- D10 assertion
----------------------------------------------------------------------

assert PublicationMonotonicity {
  all s, s2: State, d: Doc |
    (Step[s, s2] and d in s.D and s.pub[d] = Published)
      implies s2.pub[d] = Published
}

check PublicationMonotonicity for 5 but exactly 2 State

-- Non-vacuity: a published document survives a step
run NonVacuity {
  some s, s2: State, d: Doc |
    Step[s, s2] and d in s.D and s.pub[d] = Published
      and s2.pub[d] = Published
} for 5 but exactly 2 State
