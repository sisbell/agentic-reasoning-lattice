include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module ArrangementFunctional {
  import opened TumblerAlgebra

  // Two-space state (arrangement only; content store modeled per-property)
  datatype State = State(M: map<Tumbler, map<Tumbler, Tumbler>>)

  // S2 — ArrangementFunctional
  // For each document d, M(d) maps each V-position to exactly one I-address.
  // By construction: Dafny's map<Tumbler, Tumbler> is inherently functional —
  // each key has at most one value, so uniqueness is a type-level guarantee.
  ghost predicate ArrangementFunctional(s: State) {
    true
  }
}
