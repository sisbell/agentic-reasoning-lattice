include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// L1 — LinkElementLevel
module LinkElementLevel {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // L1 — LinkElementLevel
  // Every link address is an element-level tumbler: zeros(a) = 3
  ghost predicate LinkElementLevel(linkDomain: set<Tumbler>) {
    forall a :: a in linkDomain ==> TumblerHierarchy.ElementAddress(a)
  }
}
