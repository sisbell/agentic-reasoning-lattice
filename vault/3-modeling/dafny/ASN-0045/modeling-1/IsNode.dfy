include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module IsNode {
  import opened TumblerAlgebra
  import opened TumblerHierarchy

  // E.node — IsNode
  predicate IsNode(t: Tumbler) {
    ValidAddress(t) && ZeroCount(t.components) == 0
  }
}
