include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"

// L1 — LinkElementLevel
module LinkElementLevel {
  import opened TumblerAlgebra
  import TumblerHierarchy

  // L1 — LinkElementLevel
  // (A a ∈ dom(Σ.L) :: zeros(a) = 3)
  // Every link address has exactly 3 zero separators (element level).
  // Combined with T4 (ValidAddress), this gives TumblerHierarchy.ElementAddress.
  ghost predicate LinkElementLevel(linkDomain: set<Tumbler>) {
    forall a :: a in linkDomain ==> TumblerHierarchy.ZeroCount(a.components) == 3
  }
}
