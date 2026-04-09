include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module ContentAllocatable {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // Minimal state projection for K.α precondition
  datatype State = State(E: set<Tumbler>)

  // ---------------------------------------------------------------------------
  // K.α (pre) — ContentAllocatable
  //
  // IsElement(a) ∧ origin(a) ∈ E_doc
  //
  // origin(a) is the unique document-level prefix of element address a.
  // The existential is equivalent: each element address has exactly one
  // prefix with ZeroCount == 2 (document level).
  // ---------------------------------------------------------------------------

  ghost predicate ContentAllocatable(s: State, a: Tumbler) {
    TumblerHierarchy.ElementAddress(a) &&
    (exists d :: d in s.E && TumblerHierarchy.DocumentAddress(d) && IsPrefix(d, a))
  }
}
