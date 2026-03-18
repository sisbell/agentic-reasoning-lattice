// E.element — IsElement (INV, predicate(Tumbler))
// ValidAddress(t) ∧ zeros(t) = 3

include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

module IsElement {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // E.element — level definition
  predicate IsElement(t: Tumbler) {
    TumblerHierarchy.ValidAddress(t) && TumblerHierarchy.ZeroCount(t.components) == 3
  }
}
