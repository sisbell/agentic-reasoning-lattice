include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module IsDocument {
  import opened TumblerAlgebra
  import opened TumblerHierarchy

  // E.document — IsDocument
  predicate IsDocument(t: Tumbler) {
    ValidAddress(t) && ZeroCount(t.components) == 2
  }
}
