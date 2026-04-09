include "../../../../proofs/TumblerAlgebra/TumblerAlgebra.dfy"

module PartitionIndependenceModule {
  import opened TumblerAlgebra

  // ASN-0001 T10 — PartitionIndependence

  ghost predicate PartitionIndependence(p1: Tumbler, p2: Tumbler) {
    (!IsPrefix(p1, p2) && !IsPrefix(p2, p1)) ==>
    (forall a, b :: IsPrefix(p1, a) && IsPrefix(p2, b) ==> a != b)
  }

  lemma PartitionIndependenceHolds(p1: Tumbler, p2: Tumbler)
    ensures PartitionIndependence(p1, p2)
  { }
}
