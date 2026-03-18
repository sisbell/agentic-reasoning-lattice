include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module TwoSpaceSeparation {
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

  // S9 — TwoSpaceSeparation
  // No modification to any arrangement can alter the content store.
  // derived from S0
  lemma TwoSpaceSeparation(s: State, s': State, d: Tumbler)
    requires ContentImmutability(s, s')
    requires d in s.M && d in s'.M
    requires s.M[d] != s'.M[d]
    ensures forall a :: a in s.C ==> a in s'.C && s'.C[a] == s.C[a]
  { }
}
