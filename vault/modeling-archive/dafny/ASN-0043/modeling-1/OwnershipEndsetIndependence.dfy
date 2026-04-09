include "Home.dfy"
include "LinkStore.dfy"

// L2 — OwnershipEndsetIndependence
module OwnershipEndsetIndependence {
  import opened TumblerAlgebra
  import TumblerHierarchy
  import Home
  import LinkStore

  // Home parameterized by store — for stating store-independence.
  ghost function HomeFromStore(store: LinkStore.Store, a: Tumbler): Tumbler
    requires a in store
    requires TumblerHierarchy.HasElementField(a)
  {
    Home.HomeDoc(a)
  }

  // L2 — The home document of a link is determined entirely by its address
  // and is independent of the link's endsets. Replacing the link value
  // stored at address a does not change a's home document.
  // Derived from L1 (element-level), L1a (scoped allocation), T4 (field parsing).
  lemma OwnershipEndsetIndependence(
    store: LinkStore.Store, a: Tumbler, l: LinkStore.Link
  )
    requires a in store
    requires TumblerHierarchy.HasElementField(a)
    ensures HomeFromStore(store, a) == HomeFromStore(store[a := l], a)
  { }
}
