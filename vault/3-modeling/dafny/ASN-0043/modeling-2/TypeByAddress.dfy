include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"
include "LinkStore.dfy"

// L8 — TypeByAddress
module TypeByAddress {
  import opened TumblerAlgebra
  import opened LinkStore

  // same_type: type matching by endset equality (set equality of spans)
  predicate SameType(store: Store, a1: Tumbler, a2: Tumbler)
    requires a1 in store
    requires a2 in store
  {
    store[a1].typ == store[a2].typ
  }

  // L8 — TypeByAddress
  // Type matching is by address identity (structural endset equality),
  // not by dereferencing content at addressed locations.
  // Tautological by construction: SameType IS endset equality.
  ghost predicate TypeByAddress(store: Store) {
    forall a1, a2 :: a1 in store && a2 in store ==>
      (SameType(store, a1, a2) <==> store[a1].typ == store[a2].typ)
  }

  lemma TypeByAddressHolds(store: Store)
    ensures TypeByAddress(store)
  { }
}
