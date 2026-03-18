include "LinkStore.dfy"

// L8 — TypeByAddress
// Type matching is by address identity, not by content at the address.
module TypeByAddress {
  import opened LinkStore

  // same_type(a1, a2): set equality of type endsets
  ghost predicate SameType(l1: Link, l2: Link) {
    l1.typ == l2.typ
  }

  // L8 — TypeByAddress
  // For all link pairs, type equivalence is determined entirely by
  // set equality of their type endsets (span address comparison, not
  // content lookup). Holds for every store by construction.
  ghost predicate TypeByAddress(store: Store) {
    forall a1, a2 :: a1 in store && a2 in store ==>
      (SameType(store[a1], store[a2]) <==> store[a1].typ == store[a2].typ)
  }

  lemma TypeByAddressHolds(store: Store)
    ensures TypeByAddress(store)
  { }
}
