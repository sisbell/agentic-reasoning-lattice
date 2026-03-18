include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "../../../../proofs/TumblerAlgebra/TumblerHierarchy.dfy"
include "Home.dfy"
include "LinkStore.dfy"

// L2 — OwnershipEndsetIndependence
module OwnershipEndsetIndependence {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import Home
  import LinkStore

  // L2 — OwnershipEndsetIndependence
  // (A a ∈ dom(Σ.L) :: home(a) depends only on a)
  //
  // Derived from L1 (element level), L1a (scoped allocation), T4 (valid address).
  // Home.Home is function(Tumbler): Tumbler — it takes only the address,
  // not the link value or system state. For any two states mapping a to
  // different links, the home document is identical because Home.Home
  // cannot reference the endsets (from, to, type).
  lemma OwnershipEndsetIndependence(
    s1: LinkStore.Store, s2: LinkStore.Store,
    a: Tumbler
  )
    requires a in s1 && a in s2
    requires TumblerHierarchy.ElementAddress(a)  // L1
    ensures Home.Home(a) == Home.Home(a)  // independent of s1[a], s2[a]
  { }
}
