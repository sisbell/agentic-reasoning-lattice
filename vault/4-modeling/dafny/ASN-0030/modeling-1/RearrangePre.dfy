include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/Foundation/Foundation.dfy"

module RearrangePre {
  import opened TumblerAlgebra
  import opened Foundation

  // ASN-0030 A4a pre — RearrangePre (PRE, requires)
  // d ∈ Σ.D
  // Precondition for REARRANGE(d, cuts): d must be a document in the state.
  predicate RearrangePre(s: State, d: DocId) {
    d in s.docs
  }
}
