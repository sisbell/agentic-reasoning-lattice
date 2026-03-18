include "LinkStore.dfy"
include "LinkImmutability.dfy"

// L12a — LinkStoreMonotonicity
// The domain of the link store is monotonically non-decreasing.
// Derived from L12 (LinkImmutability).
module LinkStoreMonotonicity {
  import opened LinkStore
  import LI = LinkImmutability
  import opened TumblerAlgebra

  // L12a — LinkStoreMonotonicity
  // dom(before) <= dom(after) for every transition satisfying L12
  lemma LinkStoreMonotonicity(before: Store, after: Store)
    requires LI.LinkImmutability(before, after)
    ensures before.Keys <= after.Keys
  { }
}
