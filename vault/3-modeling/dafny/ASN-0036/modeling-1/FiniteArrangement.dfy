include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module FiniteArrangement {
  import opened TumblerAlgebra

  // Two-space state (arrangement only; content store modeled per-property)
  datatype State = State(M: map<Tumbler, map<Tumbler, Tumbler>>)

  // S8-fin — FiniteArrangement
  // For each document d, dom(Σ.M(d)) is finite.
  // By construction: Dafny's map<Tumbler, Tumbler> has a finite domain —
  // |M(d).Keys| is always a finite natural number, so finiteness is a
  // type-level guarantee.
  ghost predicate FiniteArrangement(s: State) {
    true
  }
}
