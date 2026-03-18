include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "Home.dfy"

module LinkScopedAllocation {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import Home

  // L1a — LinkScopedAllocation
  // Every link address is allocated under the tumbler prefix of
  // the document whose owner created it.
  ghost predicate LinkScopedAllocation(linkDomain: set<Tumbler>) {
    forall a :: a in linkDomain ==>
      TumblerHierarchy.HasElementField(a) &&
      TumblerHierarchy.DocumentAddress(Home.HomeDoc(a)) &&
      IsPrefix(Home.HomeDoc(a), a)
  }
}
