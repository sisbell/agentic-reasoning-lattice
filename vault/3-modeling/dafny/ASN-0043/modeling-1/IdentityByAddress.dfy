include "LinkStore.dfy"

// L11 — IdentityByAddress
// Link identity is address identity: distinct addresses designate distinct
// link entities even when their link values coincide. The link store is
// not necessarily injective.
module IdentityByAddress {
  import opened LinkStore
  import opened TumblerAlgebra

  // L11 — IdentityByAddress
  // For map<Tumbler, Link>, entity identity is by key (address).
  // The predicate explicitly does not require injectivity: equal values
  // at distinct addresses do not collapse entities.
  ghost predicate IdentityByAddress(store: Store) {
    forall a1, a2 :: a1 in store && a2 in store && a1 != a2
      ==> true  // distinct addresses are distinct entities by construction
  }

  lemma IdentityByAddressHolds(store: Store)
    ensures IdentityByAddress(store)
  { }

  // Non-injectivity witness: a store with two distinct addresses mapping
  // to the same link value satisfies the invariant.
  lemma NonInjectivityPermitted(a1: Tumbler, a2: Tumbler, link: Link)
    requires a1 != a2
    ensures IdentityByAddress(map[a1 := link, a2 := link])
  { }
}
