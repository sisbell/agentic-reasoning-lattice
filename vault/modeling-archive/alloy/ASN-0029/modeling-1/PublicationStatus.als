-- PublicationStatus.als
-- Σ.pub : Σ.D → {private, published, privashed}
-- State field: pub is a total function from D to three publication statuses.

sig Doc {}

abstract sig PubStatus {}
one sig Private, Published, Privashed extends PubStatus {}

sig State {
  D: set Doc,
  pub: Doc -> lone PubStatus
} {
  -- pub is defined on exactly D, with one status per document
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

-- Change publication status from private to published or privashed (D10a)
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
-- Assertions
----------------------------------------------------------------------

-- pub domain tracks D through transitions
assert PubDomainTracksD {
  all s, s2: State |
    Step[s, s2] implies s2.pub.PubStatus = s2.D
}

-- pub remains a total function on D through transitions
assert PubTotalAfterStep {
  all s, s2: State |
    Step[s, s2] implies (all d: s2.D | one s2.pub[d])
}

check PubDomainTracksD for 5 but exactly 2 State
check PubTotalAfterStep for 5 but exactly 2 State

-- Non-vacuity: all three statuses coexist in one state
run NonVacuity {
  some s: State {
    some d1, d2, d3: s.D {
      disj[d1, d2, d3]
      s.pub[d1] = Private
      s.pub[d2] = Published
      s.pub[d3] = Privashed
    }
  }
} for 5 but exactly 1 State
