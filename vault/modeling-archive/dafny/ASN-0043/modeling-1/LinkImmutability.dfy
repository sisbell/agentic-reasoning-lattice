include "LinkStore.dfy"

// L12 — LinkImmutability
// Once created, a link's address persists and its value is permanently fixed.
// Transition invariant over two states.
module LinkImmutability {
  import opened LinkStore
  import opened TumblerAlgebra

  // L12 — LinkImmutability
  // (A a : a in dom(before) : a in dom(after) /\ after[a] == before[a])
  ghost predicate LinkImmutability(before: Store, after: Store) {
    forall a :: a in before ==> a in after && after[a] == before[a]
  }
}
