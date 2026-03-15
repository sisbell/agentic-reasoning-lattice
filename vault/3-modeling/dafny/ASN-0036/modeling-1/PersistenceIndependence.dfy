include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module PersistenceIndependence {
  import opened TumblerAlgebra

  type Val(==)

  datatype State = State(
    C: map<Tumbler, Val>,
    M: map<Tumbler, map<Tumbler, Tumbler>>
  )

  // S0 — ContentImmutability (transition invariant)
  ghost predicate ContentImmutability(s: State, s': State) {
    forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  }

  // S6 — PersistenceIndependence
  // derived from S0
  lemma PersistenceIndependence(s: State, s': State, a: Tumbler)
    requires ContentImmutability(s, s')
    requires a in s.C
    ensures a in s'.C
  { }
}
