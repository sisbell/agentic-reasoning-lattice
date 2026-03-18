include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "Home.dfy"

// L1a — LinkScopedAllocation
module LinkScopedAllocation {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import Home

  // L1a — LinkScopedAllocation
  // (A a ∈ dom(Σ.L) :: origin(a) identifies the allocating document)
  // The document-level prefix of each link address is a valid document
  // address and is a prefix of the link address.
  ghost predicate LinkScopedAllocation(linkDomain: set<Tumbler>) {
    forall a :: a in linkDomain ==>
      TumblerHierarchy.DocumentAddress(Home.Home(a)) &&
      IsPrefix(Home.Home(a), a)
  }
}
