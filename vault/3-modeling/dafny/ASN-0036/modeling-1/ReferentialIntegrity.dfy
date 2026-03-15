include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ReferentialIntegrity {
  import opened TumblerAlgebra

  // Opaque content value type
  type Val(==)

  // Two-space state (content store + arrangements)
  datatype State = State(C: map<Tumbler, Val>, M: map<Tumbler, map<Tumbler, Tumbler>>)

  // S3 — ReferentialIntegrity
  // (A d, v : v ∈ dom(Σ.M(d)) : Σ.M(d)(v) ∈ dom(Σ.C))
  ghost predicate ReferentialIntegrity(s: State) {
    forall d, v :: d in s.M && v in s.M[d] ==> s.M[d][v] in s.C
  }
}
